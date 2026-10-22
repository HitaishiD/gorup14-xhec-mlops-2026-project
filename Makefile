install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

api:
	uv run uvicorn src.web_service.main:app --reload --port 8000
