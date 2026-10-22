FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Install dependencies first so this layer is cached when only the code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/
COPY bin/ bin/

ENV PATH="/app/.venv/bin:$PATH"

# 8001: FastAPI, 4201: Prefect server (mapped to 8000 and 4200 on the host)
EXPOSE 8001 4201

CMD ["bash", "bin/run_services.sh"]
