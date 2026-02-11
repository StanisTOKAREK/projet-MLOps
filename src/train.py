import pandas as pd
import joblib
import logging
import os
import random
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# --- CONFIGURATION & REPRODUCTIBILITÉ ---
# On fixe la seed pour que l'entraînement donne toujours le même résultat (Critère 3)
SEED = 42
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")

# Configuration des logs structurés (Critère 7)
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
    
    # 1. Chargement des données (On utilise Iris pour l'exemple)
    logger.info("Chargement des données...")
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    # 2. Séparation Entraînement / Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )

    # 3. Entraînement du modèle
    logger.info("Début de l'entraînement du modèle...")
    model = RandomForestClassifier(n_estimators=100, random_state=SEED)
    model.fit(X_train, y_train)

    # 4. Évaluation simple
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Entraînement terminé. Précision (Accuracy) : {acc:.4f}")

    # 5. Sauvegarde du modèle (Critère 3)
    # On s'assure que le dossier models existe
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Modèle sauvegardé avec succès dans : {MODEL_PATH}")

if __name__ == "__main__":
    train()
