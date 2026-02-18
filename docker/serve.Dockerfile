# 1. Image légère et sécurisée
FROM python:3.11-slim

RUN useradd -m mluser
WORKDIR /home/mluser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'API et du code d'inférence (Point 3)
COPY api/ ./api/
COPY src/ ./src/
RUN mkdir -p models && chown -R mluser:mluser /home/mluser

USER mluser
EXPOSE 8000

# Lancement avec Uvicorn (Point 6)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]