import requests
import redis
from flask import Flask, jsonify

# Inicializa la aplicación Flask
app = Flask(__name__)

# Conecta a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
    return "¡Bienvenido a la Pokémon App!"

@app.route('/pokemon/<int:num>')
def get_pokemon(num):
    """Consulta un Pokémon por su número en la Pokédex y almacena en Redis."""
    
    # Primero, intenta obtener el Pokémon de Redis
    cached_pokemon = r.get(f"pokemon:{num}")
    
    if cached_pokemon:
        # Si está en caché, decodifica la respuesta (Redis devuelve bytes)
        pokemon = eval(cached_pokemon.decode("utf-8"))
        return jsonify(pokemon)
    
    # Si no está en caché, consulta la API de Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{num}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon = {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [type["type"]["name"] for type in data["types"]]
        }
        
        # Almacena la respuesta en Redis para futuras consultas
        r.set(f"pokemon:{num}", str(pokemon), ex=3600)  # Guardar por 1 hora (3600 segundos)
        
        return jsonify(pokemon)
    else:
        return jsonify({"error": "Pokémon no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
