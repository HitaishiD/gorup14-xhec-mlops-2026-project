import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.metrics import root_mean_squared_error


def predict(X: pd.DataFrame, model: RegressorMixin) -> np.ndarray:
    """Predict the number of rings."""
    return model.predict(X)


def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """Root mean squared error, in rings."""
    return root_mean_squared_error(y_true, y_pred)
