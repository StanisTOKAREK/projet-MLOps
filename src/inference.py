import joblib
import os
import logging
import numpy as np

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# On récupère le chemin du modèle (via variable d'environnement ou chemin par défaut)
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")

def load_model():
    """Charge le modèle depuis le disque."""
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Modèle introuvable à l'endroit : {MODEL_PATH}")
        raise FileNotFoundError(f"Le fichier {MODEL_PATH} est absent. Lancez train.py d'abord.")
    
    model = joblib.load(MODEL_PATH)
    logger.info("Modèle chargé avec succès.")
    return model

def predict(data):
    """
    Prend des données en entrée et retourne une prédiction.
    data doit être un tableau numpy ou une liste de caractéristiques.
    """
    model = load_model()
    # On s'assure que les données sont au bon format pour sklearn
    prediction = model.predict(np.array(data).reshape(1, -1))
    return int(prediction[0])

if __name__ == "__main__":
    # Test rapide : on simule une fleur (si tu utilises le dataset Iris)
    # Exemple de caractéristiques : [sepal_length, sepal_width, petal_length, petal_width]
    test_data = [5.1, 3.5, 1.4, 0.2]
    result = predict(test_data)
    print(f"Résultat de la prédiction : {result}")
