# 1. Image légère
FROM python:3.11-slim

# 2. Sécurité : utilisateur non-root
RUN useradd -m mluser
WORKDIR /home/mluser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'API et du code source
COPY api/ ./api/
COPY src/ ./src/

# Création du dossier models (le volume sera monté ici)
RUN mkdir -p models && chown -R mluser:mluser /home/mluser

USER mluser

# Port pour l'API
EXPOSE 8000

# Lancement de l'API avec Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]