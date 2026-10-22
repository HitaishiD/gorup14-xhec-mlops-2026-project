# Team Plan — Group 14, Abalone Age Prediction

This file is the agreed plan for the project. If something here needs to change, say so in the team chat first and update this file in a PR.

**Deadline:** everything merged to `main` by end of day, **Oct 23**. Only `main` is graded.

## Team

| Role | Who | GitHub | Branches | Issues |
|---|---|---|---|---|
| A – Setup & integration | Nikolai Levin | `Nikolai-Levin` | `0/environment_setup`, final integration PR | #2, #7 |
| B – Data & model | Hitaishi Dhoowooah | `HitaishiD` | `1/eda_and_modelling_notebooks`, `2/from_notebooks_to_modules` | #3, #4 |
| C – API & Docker | Martin Dias Pinto | `mdiaspinto` | `4/deploy_model_api` | #6 |
| D – Orchestration | Guust | _TBD_ | `3/use_prefect` | #5 |

Everyone must have at least one significant commit merged into `main`.

## Rules

- **Merge commits only.** Never squash or rebase-merge. Graders read the commit history.
- **Every change goes through a PR**, reviewed by a teammate before merging. Nobody pushes to `main` directly. GitHub doesn't enforce this, so it's on us.
- **One owner per branch.** You work on the numbered template branch you own.
- **Bring in `main` before opening your PR:** `git merge origin/main`. Don't rebase or force-push.
- **Once a branch is merged**, stop committing to it.
- **Link your issue:** the PR description says `Closes #<issue>`.
- **Keep it simple.** Every line on `main` should be something its author can explain. No extra features beyond the `PR_i.md` checklists.
- **Tooling:** `uv` only (`pyproject.toml` + `uv.lock`), Python 3.11. No `requirements*.in`. Add packages with `uv add <pkg>==<version>`.
- Each `PR_i.md` file is deleted in the PR that completes it.

## Repo settings (Hitaishi, she owns the fork)

- [ ] Settings → General → Pull Requests: turn off **squash merging** and **rebase merging** (merge commits only)
- [ ] Settings → General → Features: turn on **Issues**
- [ ] When Guust arrives: add him as an **admin** collaborator

## Data

- Download the dataset manually from [Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) and save it **unchanged** as `data/abalone.csv`.
- `data/*.csv` is gitignored. The README tells graders to do the same.
- Kaggle's columns: `Sex, Length, Diameter, Height, Whole weight, Shucked weight, Viscera weight, Shell weight, Rings`.

## Shared contract

B, C and D code against this. If you need to change it, warn the others in the chat first.

**`src/modelling/`** (B writes it, D orchestrates it)

| File | Function | Does |
|---|---|---|
| `preprocessing.py` | `preprocess(df, encoder=None) -> (X, y, encoder)` | renames columns to snake_case (`whole_weight`, …), one-hot encodes `sex` with a `OneHotEncoder` (fits it if `encoder` is `None`), `y = rings` |
| `training.py` | `train_model(X, y) -> model` | fits one sklearn regressor |
| `predicting.py` | `predict(X, model) -> np.ndarray` | predicted rings |
| `utils.py` | `save_pickle(obj, path)`, `load_pickle(path)` | pickle I/O |
| `main.py` | `python -m src.modelling.main data/abalone.csv` | trains, prints the test RMSE, writes the pickles |

**Artifacts:** `src/web_service/local_objects/model.pkl` and `encoder.pkl`. They're **committed**, so the Docker image works without training first.

**API** (C writes it)

- `GET /` is a health check
- `POST /predict`
  - request: `{"sex": "M"|"F"|"I", "length": float, "diameter": float, "height": float, "whole_weight": float, "shucked_weight": float, "viscera_weight": float, "shell_weight": float}`
  - response: `{"rings": float}`

**Makefile.** Nikolai creates it, and each owner adds their own targets:

| Target | Owner |
|---|---|
| `install`, `lint` | Nikolai |
| `train` | Hitaishi |
| `prefect-server`, `deploy` | Guust |
| `api`, `docker-build`, `docker-run` | Martin |

## Order of work

```
0 env (Nikolai) ─┐
1 notebooks (Hitaishi) ─┼─> 2 modules + pickles (Hitaishi) ─┬─> 3 Prefect (Guust) ─┬─> integration (Nikolai) ─> optional model upgrade
4 API on placeholder (Martin) ──────────────────────────────┴─> 4 wired to real pickles (Martin) ─┘
```

Start now: Nikolai on `0`, Hitaishi on `1`, Martin on `4` with a placeholder model. Guust reads `lessons/03-pipeline-and-orchestration` until `2` is merged.

## Checklists

### Nikolai — `0/environment_setup`
- [ ] `pyproject.toml`: fill in the TODOs, Python `>=3.11,<3.12`, add dev and app dependencies with `uv add`
- [ ] Remove `requirements-dev.in` and any other `requirements*` files
- [ ] `.pre-commit-config.yaml`: ruff lint + format, then `uv run pre-commit install`
- [ ] `.github/workflows/ci.yaml`: run pre-commit / ruff on every PR
- [ ] `.gitignore`: add `data/*.csv`
- [ ] `Makefile` with `install` and `lint`
- [ ] README skeleton: team table, setup (`make install`), where to put `data/abalone.csv`

### Hitaishi — `1/eda_and_modelling_notebooks`
- [ ] `notebooks/eda.ipynb`: distributions, correlations, `Sex` categories
- [ ] `notebooks/modelling.ipynb`: preprocess → train one simple regressor → RMSE

### Hitaishi — `2/from_notebooks_to_modules` (after `1` is merged)
- [ ] Turn the notebook into the `src/modelling/` modules exactly as in the contract
- [ ] `make train` writes `model.pkl` + `encoder.pkl` to `src/web_service/local_objects/`, and you commit them
- [ ] Delete the stray `.pre-commit-config.yaml.yaml` on this branch
- [ ] README: how to train

### Guust — `3/use_prefect` (after `2` is merged)
- [ ] Wrap the `src/modelling` steps as Prefect `@task`s inside one `@flow`
- [ ] A deployment that retrains on a schedule
- [ ] `make prefect-server`, `make deploy`
- [ ] README: start the Prefect UI, run the deployment, see the flow runs

### Martin — `4/deploy_model_api`
- [ ] `src/web_service/lib/models.py`: Pydantic input/output schemas from the contract
- [ ] `src/web_service/lib/inference.py`: load the pickles, reuse `preprocess` + `predict`
- [ ] `src/web_service/main.py`: FastAPI with `GET /` and `POST /predict`
- [ ] Until `2` lands: train a throwaway model locally into `local_objects/` and don't commit it
- [ ] `Dockerfile.app` + `bin/run_services.sh`. Run with `-p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201`
- [ ] Once `2` is merged: `git merge origin/main`, test with the real pickles
- [ ] `make api`, `make docker-build`, `make docker-run`
- [ ] README: how to run the API in Docker, plus an example `curl` request

### Nikolai — final integration PR (after `3` and `4` are merged)
- [ ] Fresh clone + new environment, follow only the README: `make install` → `make train` → Prefect → `make docker-run` → a prediction succeeds
- [ ] No `TODO` left anywhere (`grep -rn TODO .`), no `PR_*.md`, no unused files
- [ ] The README is the final one (not the template), with every team member and GitHub ID
- [ ] Check that every team member has a significant commit on `main`

### Afterwards (optional) — model upgrade (Hitaishi)
- [ ] Only once the integration PR is merged and the clean run passes. A separate PR, with the contract unchanged
