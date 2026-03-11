# 1. Imagen base de Python ligera
FROM python:3.12-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código
COPY . .

# 5. Exponer el puerto
EXPOSE 5000

# 6. Comando para ejecutar
CMD ["flask", "run","--host=0.0.0.0", "--port=5000"]

