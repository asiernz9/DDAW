import os
from handler.command_handler import CommandHandler

class SetupHandler:
    @staticmethod
    def instalar_dependencias():
        """Instala las dependencias necesarias para la aplicación."""
        print("Instalando dependencias y configurando entorno...")
        
        # Actualizar el sistema e instalar paquetes
        CommandHandler.run_command("sudo apt update")
        CommandHandler.run_command("sudo apt install -y python3 python3-pip python3-venv nginx")

        # Crear el directorio donde estará la aplicación si no existe
        CommandHandler.run_command("sudo mkdir -p /var/www/pokemon_app")

        # Crear un entorno virtual
        CommandHandler.run_command("python3 -m venv /home/asiernz9/pokemon_app/venv")

        # Activar el entorno y instalar dependencias de Python
        CommandHandler.run_command(". /home/asiernz9/pokemon_app/venv/bin/activate && pip install Flask gunicorn")

        print("Dependencias instaladas correctamente.")

    @staticmethod
    def comprobar_existencias(file_path):
        """Comprueba si un archivo o directorio existe y lo crea si no existe."""
        if os.path.exists(file_path):
            print(f'El archivo en el directorio: {file_path} existe')
        else:
            print(f'El archivo en el directorio: {file_path} no existe. Creando...')
            # Si es un directorio, lo creamos
            if os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(file_path)
                print(f"Directorio {file_path} creado correctamente.")
            else:
                print(f"No se pudo crear el archivo {file_path}. Verifica los permisos.")

