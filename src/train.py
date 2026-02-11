import pandas as pd
import joblib
import logging
import os
import random
import numpy as np
import json  # Ajouté pour gérer le fichier metrics.json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# --- CONFIGURATION & REPRODUCTIBILITÉ ---
SEED = 42
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
METRICS_PATH = "models/metrics.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    logger.info(f"Seed fixée à : {seed}")

def train():
    set_seed()
    
    # 1. Chargement des données
    logger.info("Chargement des données...")
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    # --- POINT 5 : VALIDATION DES DONNÉES ---
    if X.empty or len(y) == 0:
        logger.error("Le dataset est vide. Arrêt de l'entraînement.")
        return
    logger.info(f"Données validées : {X.shape[0]} échantillons détectés.")

    # 2. Séparation Entraînement / Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )

    # 3. Entraînement du modèle
    logger.info("Début de l'entraînement du modèle...")
    model = RandomForestClassifier(n_estimators=100, random_state=SEED)
    model.fit(X_train, y_train)

    # 4. Évaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Entraînement terminé. Précision (Accuracy) : {acc:.4f}")

    # 5. Sauvegarde du modèle (Artefact)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Modèle sauvegardé dans : {MODEL_PATH}")

    # --- POINT 5 : VERSIONING DES MÉTRIQUES (AUTOMATIQUE) ---
    metrics = {
        "accuracy": acc,
        "model_type": "RandomForest",
        "timestamp": pd.Timestamp.now().isoformat(),
        "seed": SEED
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Métriques enregistrées dans : {METRICS_PATH}")

if __name__ == "__main__":
    train()