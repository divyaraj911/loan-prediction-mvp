# src/app.py
import os
import pickle
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Initialize our FastAPI app core engine
app = FastAPI(
    title="Loan Default Prediction Service",
    version="1.0.0",
    description="Production ML API for evaluating credit risk profiles."
)

MODEL_PATH = "models/loan_model.pkl"
model = None

# Telemetry counters to track application performance live
metrics = {
    "total_predictions": 0,
    "total_defaults_predicted": 0,
    "start_time": time.time()
}

# Define what an incoming request should look like (Validation layer)
class ApplicantData(BaseModel):
    income: float = Field(..., example=65000.0, description="Annual gross income")
    credit_score: int = Field(..., ge=300, le=850, example=710, description="Applicant Credit Score")
    loan_amount: float = Field(..., example=15000.0, description="Requested principal amount")

@app.on_event("startup")
def load_model_asset():
    """This runs automatically when the web server boots up."""
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Artifact not found at {MODEL_PATH}. Run training first.")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Inference model asset cached successfully into memory.")

@app.get("/health")
def health_check():
    """Liveness probe validating api availability."""
    if model is None:
        return {"status": "unhealthy", "error": "Model not loaded"}, 503
    return {"status": "healthy", "uptime_seconds": round(time.time() - metrics["start_time"], 2)}

@app.get("/metrics")
def get_metrics():
    """Provides monitoring hooks for custom scraper monitoring scripts."""
    return {
        "metrics": metrics,
        "environment": os.getenv("ENV", "production")
    }

@app.post("/predict")
def predict_risk(data: ApplicantData):
    """Processes applicant features and evaluates transaction risk."""
    global model
    if not model:
        raise HTTPException(status_code=503, detail="Model pipeline is unavailable.")
    
    try:
        # Format the incoming user data into a 2D array that scikit-learn expects
        features = [[data.income, data.credit_score, data.loan_amount]]
        
        # Predict 0 (Safe) or 1 (Will Default)
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][prediction])
        
        # Increment our metrics live trackers
        metrics["total_predictions"] += 1
        if prediction == 1:
            metrics["total_defaults_predicted"] += 1
            
        return {
            "default_prediction": prediction,
            "probability": round(probability, 4),
            "risk_assessment": "High Risk" if prediction == 1 else "Low Risk"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")