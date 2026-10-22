from fastapi import FastAPI

from src.web_service.lib.inference import run_inference
from src.web_service.lib.models import AbaloneFeatures, Prediction

app = FastAPI(
    title="Abalone Age Prediction",
    description="Predict the number of rings of an abalone from its physical measurements.",
)


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=Prediction, status_code=201)
def predict(payload: AbaloneFeatures) -> dict:
    return {"rings": run_inference(payload)}
