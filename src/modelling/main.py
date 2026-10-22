# Training flow: read the data, preprocess it, train a model, then pickle the model and encoder.

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split

from src.modelling.predicting import predict
from src.modelling.preprocessing import preprocess
from src.modelling.training import train_model
from src.modelling.utils import save_pickle

LOCAL_OBJECTS = Path("src/web_service/local_objects")


def main(trainset_path: Path) -> None:
    """Train a model on the data at `trainset_path`, print the test RMSE and pickle the model and encoder."""
    df = pd.read_csv(trainset_path)
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    X_train, y_train, encoder = preprocess(df_train)
    X_test, y_test, _ = preprocess(df_test, encoder)

    model = train_model(X_train, y_train)
    rmse = root_mean_squared_error(y_test, predict(X_test, model))
    print(f"Test RMSE: {rmse:.3f}")

    save_pickle(model, LOCAL_OBJECTS / "model.pkl")
    save_pickle(encoder, LOCAL_OBJECTS / "encoder.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=Path, help="Path to the training set")
    args = parser.parse_args()
    main(args.trainset_path)
