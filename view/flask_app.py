from flask import Flask, render_template, jsonify, request
import requests
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def home():
    try:
        logger.info("Intentando obtener la lista de Pokémon...")
        response = requests.get(f"{POKEMON_API_URL}?limit=151")
        response.raise_for_status()  # Esto lanzará una excepción si hay un error HTTP
        
        data = response.json()
        pokemon_list = []
        
        for i, pokemon in enumerate(data["results"]):
            pokemon_id = i + 1
            pokemon_list.append({
                "id": pokemon_id,
                "name": pokemon["name"],
                "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
            })
        
        logger.info(f"Se obtuvieron {len(pokemon_list)} Pokémon exitosamente")
        return render_template('index.html', pokemon_list=pokemon_list)
    
    except requests.RequestException as e:
        logger.error(f"Error al hacer la petición a la API: {str(e)}")
        return f"Error al conectar con la API de Pokémon: {str(e)}", 500
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return f"Error inesperado: {str(e)}", 500

@app.route('/pokemon/type/<string:pokemon_type>')
def get_pokemon_by_type(pokemon_type):
    try:
        logger.info(f"Buscando Pokémon de tipo: {pokemon_type}")
        url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
        response = requests.get(url)
        response.raise_for_status()
        
        pokemon_data = response.json()
        pokemon_list = [
            {
                "id": int(pokemon["pokemon"]["url"].split('/')[-2]),
                "name": pokemon["pokemon"]["name"]
            }
            for pokemon in pokemon_data["pokemon"]
            if int(pokemon["pokemon"]["url"].split('/')[-2]) <= 151
        ]
        pokemon_list.sort(key=lambda x: x["id"])
        
        logger.info(f"Se encontraron {len(pokemon_list)} Pokémon de tipo {pokemon_type}")
        return jsonify(pokemon_list)
    
    except requests.RequestException as e:
        logger.error(f"Error al hacer la petición a la API para el tipo {pokemon_type}: {str(e)}")
        return jsonify({"error": f"Error al obtener Pokémon de tipo {pokemon_type}"}), 500
    except Exception as e:
        logger.error(f"Error inesperado al buscar por tipo {pokemon_type}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)