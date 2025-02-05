import subprocess

class CommandHandler:
    @staticmethod
    def run_command(command):
        """Ejecuta un comando del sistema."""
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Comando ejecutado correctamente: {command}")
            print(f"Salida: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando {command}: {e}")
            print(f"Error: {e.stderr}")
            raise

