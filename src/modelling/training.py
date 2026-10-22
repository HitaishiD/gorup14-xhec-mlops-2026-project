import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.linear_model import LinearRegression


def train_model(
    X: pd.DataFrame, y: pd.Series, model: RegressorMixin | None = None
) -> RegressorMixin:
    """Fit a sklearn regressor (a linear regression by default, the best model in the notebook)."""
    if model is None:
        model = LinearRegression()
    return model.fit(X, y)
