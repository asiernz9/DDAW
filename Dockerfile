FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y sudo


# Exponer el puerto de la aplicación Flask
EXPOSE 5000

# Ejecutar el servidor de Flask
CMD ["python", "main.py"]

