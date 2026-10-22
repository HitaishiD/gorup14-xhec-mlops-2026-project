from pathlib import Path

import pandas as pd

from src.modelling.predicting import predict
from src.modelling.preprocessing import preprocess
from src.modelling.utils import load_pickle
from src.web_service.lib.models import AbaloneFeatures

LOCAL_OBJECTS = Path(__file__).resolve().parents[1] / "local_objects"

# Loaded once at import, so a missing pickle fails at startup rather than on the first request
model = load_pickle(LOCAL_OBJECTS / "model.pkl")
encoder = load_pickle(LOCAL_OBJECTS / "encoder.pkl")


def run_inference(features: AbaloneFeatures) -> float:
    df = pd.DataFrame([features.model_dump()])
    X, _, _ = preprocess(df, encoder)
    return float(predict(X, model)[0])
