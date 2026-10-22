install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

train:
	uv run python -m src.modelling.main data/abalone.csv

prefect-server:
	uv run prefect server start

deploy:
	PREFECT_API_URL=http://127.0.0.1:4200/api uv run python -m src.modelling.deployment
