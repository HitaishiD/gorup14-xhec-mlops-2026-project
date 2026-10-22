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

api:
	uv run uvicorn src.web_service.main:app --reload --port 8000

docker-build:
	docker build -f Dockerfile.app -t abalone-api .

docker-run:
	docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api
