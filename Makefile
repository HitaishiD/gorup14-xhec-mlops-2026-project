install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

api:
	uv run uvicorn src.web_service.main:app --reload --port 8000

docker-build:
	docker build -f Dockerfile.app -t abalone-api .

docker-run:
	docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api
