import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin


def predict(X: pd.DataFrame, model: RegressorMixin) -> np.ndarray:
    """Return the predicted number of rings."""
    return model.predict(X)
