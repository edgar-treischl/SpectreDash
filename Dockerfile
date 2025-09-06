# Base Python
FROM python:3.12-slim-bullseye AS builder

ENV POETRY_VERSION=2.1.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install necessary OS dependencies for building Python extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry (v1.x)
RUN pip install "poetry==$POETRY_VERSION"

# For safety, ensure Poetry is on the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files for better layer caching
COPY  README.md pyproject.toml poetry.lock ./

# Copy your application code
COPY src/ ./src/


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi



# -------- Runtime Stage --------
FROM python:3.12-slim-bullseye

WORKDIR /app
ENV PYTHONPATH=/app/src

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src ./src/

EXPOSE 8000

CMD ["shiny", "run", "--reload", "--host", "0.0.0.0", "--port", "8000", "spectredash.app"]

