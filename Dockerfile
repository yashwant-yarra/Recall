FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.12.9 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md ./
COPY src/ ./src/
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["sh", "-c", "exec uvicorn recall.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
