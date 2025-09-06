# ----------- STAGE 1: Build -----------
FROM python:3.12-slim AS builder

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --only main

COPY src/ ./src/

# ----------- STAGE 2: Runtime -----------
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src ./src

EXPOSE 8000

CMD ["shiny", "run", "--reload", "--port", "8000", "spectredash.app"]
