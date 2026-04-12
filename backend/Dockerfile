FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.3.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

COPY backend/app         ./backend/app
COPY backend/alembic     ./backend/alembic
COPY backend/alembic.ini ./backend/alembic.ini
COPY scripts/            ./scripts/

RUN poetry install --only main

WORKDIR /app/backend

EXPOSE 5000

CMD ["sh", "-c", "alembic upgrade head && python -m app"]
