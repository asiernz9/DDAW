import os
from handler.command_handler import CommandHandler

class SetupHandler:
    @staticmethod
    def instalar_dependencias():
        """Instala las dependencias necesarias para la aplicación."""
        CommandHandler.run_command("sudo apt update")
        CommandHandler.run_command("sudo apt install -y python3 python3-pip python3-venv nginx")
        CommandHandler.run_command("mkdir -p /var/www/pokemon_app")
        CommandHandler.run_command("python3 -m venv /var/www/pokemon_app/venv")
        CommandHandler.run_command(
            "source /var/www/pokemon_app/venv/bin/activate && pip install Flask gunicorn"
        )
    
    @staticmethod
    def comprobar_existencias(file_path):
        """Comprueba si un archivo o directorio existe."""
        if os.path.exists(file_path):
            print(f'El archivo en el directorio: {file_path} existe')
        else:
            print(f'El archivo en el directorio: {file_path} no existe')
