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
