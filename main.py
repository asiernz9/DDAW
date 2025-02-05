import os
from handler.setup_handler import SetupHandler
from view.flask_app import app  # Esto importa la instancia 'app' de Flask

def main():
    # Paso 1: Instalación de dependencias
    print("Instalando dependencias...")
    SetupHandler.instalar_dependencias()

    # Paso 2: Comprobar si el directorio /var/www/pokemon existe
    directorio = '/var/www/pokemon'
    print(f"Comprobando existencia de {directorio}...")
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe. Creándolo...")
        os.makedirs(directorio)

    # Paso 3: Configurar la aplicación Flask (ahora ya está configurada en flask_app.py)
    print("¡Aplicación configurada correctamente!")
    app.run(debug=True)  # Arrancar la aplicación Flask

if __name__ == '__main__':
    main()


