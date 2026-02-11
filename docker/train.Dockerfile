# 1. Image légère (Point 4 : sans tag latest)
FROM python:3.11-slim

# 2. Sécurité : création d'un utilisateur non-root (Point 4)
RUN useradd -m mluser
WORKDIR /home/mluser

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et création du dossier pour le modèle
COPY src/ ./src/
RUN mkdir -p models && chown -R mluser:mluser /home/mluser

# 3. Passage à l'utilisateur non-root
USER mluser

# 4. Variables d'environnement (Point 8)
ENV MODEL_PATH=/home/mluser/models/model.joblib

# Exécution du script d'entraînement
CMD ["python", "src/train.py"]