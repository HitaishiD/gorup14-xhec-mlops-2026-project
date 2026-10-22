import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(X: pd.DataFrame, y: pd.Series) -> LinearRegression:
    """Fit a linear regression that predicts the number of rings."""
    model = LinearRegression()
    model.fit(X, y)
    return model
