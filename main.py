import os
from handler.setup_handler import SetupHandler

def main():
    # Aquí movemos la importación para evitar el ciclo
    from view.flask_app import app  # Solo importamos app aquí, después de las configuraciones previas.

    # Paso 1: Instalación de dependencias
    print("Instalando dependencias...")
    SetupHandler.instalar_dependencias()

    # Paso 2: Comprobar si el directorio /var/www/pokemon existe
    directorio = '/var/www/pokemon'
    print(f"Comprobando existencia de {directorio}...")
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe. Creándolo...")
        os.makedirs(directorio)

    # Paso 3: Configurar la aplicación Flask
    print("¡Aplicación configurada correctamente!")
    app.run(debug=True, host="0.0.0.0", port=8000)  # Ahora escucha en todas las interfaces en el puerto 8000

if __name__ == '__main__':
    main()



