from flask import Flask, render_template, jsonify, request
import requests
import logging
from functools import lru_cache
import redis

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"

# Configurar Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Cache de solicitudes
@lru_cache(maxsize=200)
def get_pokemon_details(url):
    try:
        logger.debug(f"Fetching data from: {url}")
        cached_data = redis_client.get(url)
        if cached_data:
            logger.debug(f"Cache hit for URL: {url}")
            return cached_data

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        redis_client.set(url, data)
        logger.debug(f"Cache set for URL: {url}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for URL {url}: {e}")
        raise

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {e}")
    return render_template('error.html', error=str(e)), 500

@app.route('/')
def home():
    try:
        logger.info("Fetching Pokémon list...")
        response = requests.get(f"{POKEMON_API_URL}?limit=151")
        response.raise_for_status()
        data = response.json()

        pokemon_list = []
        for i, pokemon in enumerate(data["results"], start=1):
            try:
                pokemon_details = get_pokemon_details(pokemon["url"])
                types = [t["type"]["name"] for t in pokemon_details["types"]]

                pokemon_list.append({
                    "id": i,
                    "name": pokemon["name"],
                    "types": types,
                    "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png",
                    "back_image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{i}.png"
                })
            except Exception as e:
                logger.warning(f"Failed to fetch details for {pokemon['name']}: {e}")

        logger.info(f"Fetched {len(pokemon_list)} Pokémon successfully.")
        return render_template('index.html', pokemon_list=pokemon_list)

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return render_template('error.html', error="Failed to fetch Pokémon list. Please try again later."), 500

@app.route('/pokemon/type/<string:pokemon_type>')
def get_pokemon_by_type(pokemon_type):
    try:
        logger.info(f"Fetching Pokémon of type: {pokemon_type}")
        url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pokemon_list = []
        for pokemon_entry in data["pokemon"]:
            pokemon_id = int(pokemon_entry["pokemon"]["url"].split('/')[-2])
            if pokemon_id <= 151:
                try:
                    pokemon_details = get_pokemon_details(pokemon_entry["pokemon"]["url"])
                    types = [t["type"]["name"] for t in pokemon_details["types"]]

                    pokemon_list.append({
                        "id": pokemon_id,
                        "name": pokemon_entry["pokemon"]["name"],
                        "types": types,
                        "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                        "back_image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon_id}.png"
                    })
                except Exception as e:
                    logger.warning(f"Failed to fetch details for {pokemon_entry['pokemon']['name']}: {e}")

        pokemon_list.sort(key=lambda x: x["id"])
        logger.info(f"Found {len(pokemon_list)} Pokémon of type {pokemon_type}.")
        return jsonify(pokemon_list)

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch Pokémon of type {pokemon_type}: {e}")
        return jsonify({"error": "Failed to fetch Pokémon of the specified type."}), 500

@app.route('/pokemon/types')
def get_pokemon_by_types():
    types = request.args.get('types')
    if not types:
        return jsonify({"error": "No types provided"}), 400

    types = types.split(',')
    if not all(t in ['water', 'fire'] for t in types):
        return jsonify({"error": "Only 'water' and 'fire' types are supported"}), 400

    pokemon_list = []
    for pokemon_type in types:
        try:
            logger.info(f"Fetching Pokémon of type: {pokemon_type}")
            url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for pokemon_entry in data["pokemon"]:
                pokemon_id = int(pokemon_entry["pokemon"]["url"].split('/')[-2])
                if pokemon_id <= 151:
                    try:
                        pokemon_details = get_pokemon_details(pokemon_entry["pokemon"]["url"])
                        types = [t["type"]["name"] for t in pokemon_details["types"]]

                        pokemon_list.append({
                            "id": pokemon_id,
                            "name": pokemon_entry["pokemon"]["name"],
                            "types": types,
                            "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                            "back_image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon_id}.png"
                        })
                    except Exception as e:
                        logger.warning(f"Failed to fetch details for {pokemon_entry['pokemon']['name']}: {e}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch Pokémon of type {pokemon_type}: {e}")
            return jsonify({"error": f"Failed to fetch Pokémon of type {pokemon_type}"}), 500

    pokemon_list.sort(key=lambda x: x["id"])
    logger.info(f"Found {len(pokemon_list)} Pokémon of types {types}.")
    return jsonify(pokemon_list)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
