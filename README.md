# MLOps Project: Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)

Predict the age (number of rings) of abalone from physical measurements.

## Team

| Name | GitHub |
|---|---|
| Nikolai Levin | [Nikolai-Levin](https://github.com/Nikolai-Levin) |
| Hitaishi Dhoowooah | [HitaishiD](https://github.com/HitaishiD) |
| Martin Dias Pinto | [mdiaspinto](https://github.com/mdiaspinto) |
| Guust | _TBD_ |

## Setup

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/) and `make`.

```bash
make install   # creates .venv with Python 3.11 and installs the pre-commit hooks
make lint      # runs the pre-commit hooks (ruff lint + format) on all files
```

## Data

Download the [Kaggle abalone dataset](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) and save it, unchanged, as `data/abalone.csv`. The data is not committed (`data/*.csv` is gitignored).

## Prediction API

The API serves the model and encoder committed in `src/web_service/local_objects/`, so no training is needed to run it. It requires [Docker](https://docs.docker.com/get-docker/) to be running.

```bash
make docker-build   # builds the image from Dockerfile.app
make docker-run     # starts the API and the Prefect server
```

- API: http://localhost:8000 (interactive docs at http://localhost:8000/docs)
- Prefect UI: http://localhost:4200

Example request:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sex": "M", "length": 0.455, "diameter": 0.365, "height": 0.095, "whole_weight": 0.514, "shucked_weight": 0.2245, "viscera_weight": 0.101, "shell_weight": 0.15}'
```

The response is the predicted number of rings, e.g. `{"rings": 9.3}`. `sex` must be `"M"`, `"F"` or `"I"`.

To run the API without Docker, use `make api` (same port, reloads on code changes).
