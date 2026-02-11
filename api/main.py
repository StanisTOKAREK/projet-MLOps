from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.inference import load_model
import numpy as np
import time

# 1. Définition de l'application
app = FastAPI(title="MLOps Prediction API")

# 2. Variable globale pour stocker le modèle
model = None

# 3. Modèle de données pour valider les entrées (Critère 8)
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# 4. Chargement du modèle au démarrage (Critère 6)
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

@app.get("/health")
def health_check():
    """Vérifie si l'API est fonctionnelle (Critère 6)"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/predict")
def predict(data: IrisData):
    """Prédit la classe à partir des données envoyées (Critère 6)"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    try:
        # Conversion des données d'entrée en format liste pour le modèle
        input_data = [
            data.sepal_length, 
            data.sepal_width, 
            data.petal_length, 
            data.petal_width
        ]
        
        # Inférence
        prediction = model.predict(np.array(input_data).reshape(1, -1))
        
        return {
            "prediction": int(prediction[0]),
            "model_version": "v1"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
