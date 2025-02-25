from flask import Flask, render_template, jsonify, request
import requests
import logging
from functools import lru_cache
import redis
import os
import json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Configurar Sentry
sentry_sdk.init(
    dsn="https://70895089fc56bba10cdeb2580cee80f308deebd3a0a883ffbee37e21ee50546f@sentry.io/123456",  # Sustituye con tu token completo
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,  # Ajusta esto dependiendo de cómo quieras manejar el muestreo de trazas
)

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"

# Configurar Redis correctamente (para Docker)
REDIS_HOST = os.getenv("REDIS_HOST", "pokemon-redis")
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

# Cache de solicitudes con Redis
def get_pokemon_details(url):
    try:
        logger.info(f"Fetching data from: {url}")
        
        # Verificar si ya existe en cache Redis
        cached_data = redis_client.get(url)
        if cached_data:
            logger.info(f"Cache hit for URL: {url}")
            return json.loads(cached_data)  # Convertir JSON string a diccionario
        
        # Si no está en cache, hacer la petición
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Guardar en Redis (convertido a JSON)
        redis_client.set(url, json.dumps(data))

        logger.info(f"Cache set for URL: {url}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for URL {url}: {e}")
        raise

# Manejo de errores
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {e}")
    # Reportar el error a Sentry
    sentry_sdk.capture_exception(e)
    return jsonify({"error": str(e)}), 500

# Ruta principal
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
        sentry_sdk.capture_exception(e)  # Reportar la excepción a Sentry
        return jsonify({"error": "Failed to fetch Pokémon list. Please try again later."}), 500

# Ruta para filtrar Pokémon por tipo
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
            if pokemon_id <= 151:  # Solo primeros 151 Pokémon
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
        sentry_sdk.capture_exception(e)  # Reportar la excepción a Sentry
        return jsonify({"error": "Failed to fetch Pokémon of the specified type."}), 500

# Ruta para filtrar Pokémon por múltiples tipos
@app.route('/pokemon/types', methods=["GET"])
def get_pokemon_by_types():
    # Obtener los tipos de los parámetros de la URL
    types = request.args.get('types')  # "types" es el parámetro en la URL
    if not types:
        return jsonify({"error": "No types provided"}), 400

    # Convertir los tipos en una lista (separados por comas)
    types = types.split(',')
    # Validar que los tipos estén entre los tipos permitidos de Pokémon
    allowed_types = ['water', 'fire', 'electric', 'grass', 'bug', 'ghost', 'fighting', 'psychic', 'dragon', 'dark', 'ice', 'flying']
    if not all(t in allowed_types for t in types):
        return jsonify({"error": "Invalid types provided"}), 400

    pokemon_list = []
    for pokemon_type in types:
        try:
            logger.info(f"Fetching Pokémon of type: {pokemon_type}")
            url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
            data = response.json()

            # Recorrer todos los Pokémon de ese tipo
            for pokemon_entry in data["pokemon"]:
                pokemon_id = int(pokemon_entry["pokemon"]["url"].split('/')[-2])
                if pokemon_id <= 151:  # Limitar a los primeros 151 Pokémon
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
            sentry_sdk.capture_exception(e)  # Reportar la excepción a Sentry
            return jsonify({"error": f"Failed to fetch Pokémon of type {pokemon_type}"}), 500

    pokemon_list.sort(key=lambda x: x["id"])  # Ordenar por ID de Pokémon
    logger.info(f"Found {len(pokemon_list)} Pokémon of types {types}.")
    return jsonify(pokemon_list)

# Inicio del servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8808)


