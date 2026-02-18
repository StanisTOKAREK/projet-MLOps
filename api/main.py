from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.inference import load_model # (Point 3 : Inférence séparée)
import numpy as np
import time
import logging

# Configuration des logs (Point 7 : Observabilité)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MLOps Prediction API")
model = None

# Modèle de données (Point 8 : Validation des entrées via Pydantic)
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Chargement au démarrage (Point 6)
@app.on_event("startup")
def startup_event():
    global model
    try:
        model = load_model()
        logger.info("Modèle chargé avec succès.")
    except Exception as e:
        logger.error(f"Erreur au chargement du modèle : {e}")

# Middleware pour les métriques de latence (Point 7)
@app.middleware("http")
async def log_latency(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    logger.info(f"Path: {request.url.path} | Latency: {latency:.4f}s")
    return response

# Endpoint de santé (Point 6)
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# Endpoint de prédiction (Point 6)
@app.post("/predict")
def predict(data: IrisData):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    # Conversion et Inférence
    input_data = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    prediction = model.predict(input_data)
    
    return {
        "prediction": int(prediction[0]),
        "model_version": "v1"
    }