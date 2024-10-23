# Usar una imagen de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app a la imagen
COPY . .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto que utiliza Streamlit
EXPOSE 8501

# Comando para ejecutar la app de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]