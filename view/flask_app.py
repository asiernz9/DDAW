from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URL base de la API de Pokémon
POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def home():
    return "Bienvenido a la API de Pokémon. Usa el ID del Pokémon en la URL para obtener su nombre."

@app.route('/pokemon/<int:pokemon_id>')
def get_pokemon(pokemon_id):
    # Solicitar información sobre el Pokémon desde la API externa (Pokémon API)
    url = f"{POKEMON_API_URL}{pokemon_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Obtener los datos del Pokémon
        pokemon_data = response.json()
        pokemon_name = pokemon_data["name"]
        return jsonify({"id": pokemon_id, "name": pokemon_name})
    else:
        return jsonify({"error": "Pokémon no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)





