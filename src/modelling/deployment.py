# Deployment: serve the training flow so Prefect retrains the model every day at midnight (UTC).

from src.modelling.main import training_flow

if __name__ == "__main__":
    training_flow.serve(
        name="retraining",
        cron="0 0 * * *",
        parameters={"trainset_path": "data/abalone.csv"},
    )
