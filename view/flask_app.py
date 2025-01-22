class FlaskAppSetup:
    @staticmethod
    def configurar_flask_app():
        """Configura el código base de la aplicación Flask."""
        app_code = """
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Bienvenido a la Pokémon App!"

if __name__ == '__main__':
    app.run()
"""
        file_path = "/var/www/pokemon_app/app.py"
        with open(file_path, "w") as f:
            f.write(app_code)
        print(f"Aplicación Flask configurada en {file_path}")
