FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de la aplicación Flask
EXPOSE 8000

# Ejecutar el servidor de Flask
CMD ["python", "flask_app.py"]

