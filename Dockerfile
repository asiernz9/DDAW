# Usa una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt . 

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar pytest para las pruebas
RUN pip install pytest

# Copiar todo el resto de los archivos de la aplicación
COPY . . 

# Asegurar que el archivo flask_app.py existe
RUN test -f flask_app.py || (echo "Error: flask_app.py no encontrado" && exit 1)

# Exponer el puerto en el que Flask escuchará
EXPOSE 8000

# Comando para ejecutar la aplicación Flask
CMD ["python", "flask_app.py"]




