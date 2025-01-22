import os
import subprocess

class CommandHandler:
    @staticmethod
    def run_command(command, get_output=False):
        """Ejecuta comandos en la terminal."""
        if get_output:
            return subprocess.check_output(command, shell=True, text=True)
        else:
            os.system(command)
