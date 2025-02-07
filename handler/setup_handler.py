import os
import subprocess

class SetupHandler:

    @staticmethod
    def instalar_dependencias():
        """Función para instalar las dependencias necesarias"""
        try:
            print("Instalando dependencias...")
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            print("Dependencias instaladas correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar dependencias: {e}")
            exit(1)  # Salir si las dependencias no se pudieron instalar
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            exit(1)

    # Otras funciones relacionadas con la configuración



