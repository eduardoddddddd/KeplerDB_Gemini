# Usa una imagen oficial de Python ligera
FROM python:3.12-slim

# Instalar dependencias del sistema para pyswisseph
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Hugging Face Spaces
EXPOSE 7860

# Comando para arrancar con Gunicorn
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app.app:app"]
