install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

train:
	uv run python -m src.modelling.main data/abalone.csv
