import pandas as pd
import joblib
import logging
import os
import random
import numpy as np
import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Configuration & Reproductibilité (Point 3 & 5)
SEED = 42
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
METRICS_PATH = "models/metrics.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    logger.info(f"Seed fixée à : {seed} (Critère de reproductibilité)")

def train():
    set_seed()
    
    # Chargement et validation (Point 5)
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    # Entraînement
    logger.info("Début de l'entraînement...")
    model = RandomForestClassifier(n_estimators=100, random_state=SEED)
    model.fit(X_train, y_train)

    # Évaluation et Sauvegarde des métriques (Point 5)
    acc = accuracy_score(y_test, model.predict(X_test))
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH) # Artefact modèle (Point 3)

    metrics = {
        "accuracy": acc,
        "timestamp": pd.Timestamp.now().isoformat(),
        "seed": SEED
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    
    logger.info(f"Entraînement réussi - Accuracy: {acc:.4f}")

if __name__ == "__main__":
    train()