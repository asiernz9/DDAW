from handler.setup_handler import SetupHandler
from view.flask_app import FlaskAppSetup

def main():
    # Instalación de dependencias
    SetupHandler.instalar_dependencias()
    
    # Comprobar si el directorio existe
    SetupHandler.comprobar_existencias('/var/www/pokemon')
    
    # Configurar la aplicación Flask
    FlaskAppSetup.configurar_flask_app()

if __name__ == '__main__':
    main()
