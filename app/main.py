from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pickle
import logging
from typing import List, Optional
import time
from datetime import datetime
import os

# ---------- CONFIGURE LOGGING ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- FASTAPI APP ----------
app = FastAPI(title="Hand Gesture Recognition API", version="1.0.0")

# Allow CORS (all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
# ---------- GLOBAL START TIME ----------
app_start_time = time.time()

# ---------- LOAD MODEL AND ENCODER ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "best_model_svm.pkl")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(encoder_path, "rb") as f:
        label_encoder = pickle.load(f)
    logger.info("Model and encoder loaded successfully")
except Exception as e:
    logger.error(f"Error loading model or encoder: {e}")
    model = None
    label_encoder = None

# ---------- GESTURE TO DIRECTION MAPPING ----------
GESTURE_MAPPING = {
    'like': 'up',
    'dislike': 'down',
    'two_up': 'right',
    'two_up_inverted': 'left',
}

# ---------- DATA MODELS ----------
class LandmarkData(BaseModel):
    landmarks: List[float]  # 63 values: 21 landmarks * 3 coordinates

class PredictionResponse(BaseModel):
    gesture: str
    direction: Optional[str]
    confidence: float
    timestamp: str

# ---------- METRICS STORAGE ----------
prediction_count = 0
error_count = 0
latency_sum = 0.0

# ---------- HEALTH CHECK ----------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

# ---------- PREDICTION ENDPOINT ----------
@app.post("/predict")
async def predict_gesture(request: Request):
    global prediction_count, error_count, latency_sum

    start_time = time.time()
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvv")

    # Input validation (before try-catch to avoid being caught by the generic exception handler)
    if model is None or label_encoder is None:
        raise HTTPException(status_code=500, detail="Model or encoder not loaded")

    try:
        data = await request.json()
        landmarks = data.get("landmarks")
        
        if not landmarks or len(landmarks) != 63:
            logger.error(f"Invalid input length: expected 63 landmarks, got {len(landmarks) if landmarks else 'none'}")
            raise HTTPException(status_code=400, detail="Expected 63 landmark features")

        features = np.array(landmarks).reshape(1, -1)
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))

        gesture = label_encoder.inverse_transform([prediction])[0]
        direction = GESTURE_MAPPING.get(gesture, None)

        latency = time.time() - start_time
        latency_sum += latency
        prediction_count += 1

        logger.info(f"Prediction: {gesture} → {direction} (confidence: {confidence:.3f})")
        print("oooooooooooooooooooooooo")

        return {
            "gesture": gesture,
            "direction": direction,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        error_count += 1
        logger.error(f"Prediction error: {str(e)}")
        print("kkkkkkkkkkkkkkkkkkkkkkkk")
        raise HTTPException(status_code=500, detail=str(e))


# ---------- METRICS ENDPOINT ----------
@app.get("/app-metrics")
async def get_metrics():
    avg_latency = latency_sum / prediction_count if prediction_count > 0 else 0.0

    return {
        "model_metrics": {
            "prediction_count": prediction_count,
            "error_count": error_count,
            "error_rate": error_count / max(prediction_count, 1),
            "average_latency": avg_latency
        },
        "data_metrics": {
            "input_validation_errors": error_count,
            "last_prediction_time": datetime.now().isoformat()
        },
        "server_metrics": {
            "uptime": time.time() - app_start_time,
            "status": "running"
        }
    }

# ---------- RUN SERVER LOCALLY ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)