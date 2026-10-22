# Training flow: read the data, preprocess it, train a model, then pickle the model and encoder.
# Each step is a Prefect task, so every run shows up step by step in the Prefect UI.

import argparse
from pathlib import Path

import pandas as pd
from prefect import flow, task
from sklearn.model_selection import train_test_split

from src.modelling.predicting import evaluate_model, predict
from src.modelling.preprocessing import preprocess
from src.modelling.training import train_model
from src.modelling.utils import save_pickle

LOCAL_OBJECTS = Path("src/web_service/local_objects")

# The modelling functions stay plain Python so the API can import them without Prefect
preprocess_task = task(preprocess)
train_model_task = task(train_model)
predict_task = task(predict)
evaluate_model_task = task(evaluate_model)
save_pickle_task = task(save_pickle)


@task
def load_data(path: Path) -> pd.DataFrame:
    """Load the abalone dataset."""
    return pd.read_csv(path)


@flow(log_prints=True)
def training_flow(trainset_path: Path) -> None:
    """Train a model on the data at `trainset_path`, print the test RMSE and pickle the model and encoder."""
    df = load_data(trainset_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    X_train, y_train, encoder = preprocess_task(train_df)
    X_test, y_test, _ = preprocess_task(test_df, encoder)

    model = train_model_task(X_train, y_train)
    print(f"Test RMSE: {evaluate_model_task(y_test, predict_task(X_test, model)):.3f}")

    save_pickle_task(model, LOCAL_OBJECTS / "model.pkl")
    save_pickle_task(encoder, LOCAL_OBJECTS / "encoder.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=Path, help="Path to the training set")
    args = parser.parse_args()
    training_flow(args.trainset_path)
