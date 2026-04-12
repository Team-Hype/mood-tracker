# Mood Tracker

A lightweight internal tool for agile teams to monitor collective well‑being.
Track moods, visualise trends, and gain actionable insights before sprint planning.

## Features

- **Mood logging** – choose from five moods (Rough 😡 … Great 😄) with optional comments
- **User‑specific analytics** – average mood, history, and personalised insights
- **Data visualisation** – distribution charts and daily mood trends
- **REST API** – fully documented OpenAPI endpoints (Swagger UI)
- **Dockerised** – run backend, frontend, and database with a single command

## Tech Stack

| Component   | Technologies |
|-------------|--------------|
| Backend     | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, Uvicorn |
| Frontend    | Streamlit, Pandas, Altair |
| Database    | PostgreSQL 17 (asyncpg) |
| DevOps      | Docker, GitHub Actions (lint, test, security, code quality) |
| Tooling     | Poetry, Ruff, mypy, Black, pre‑commit, pytest |

## Getting Started

### Prerequisites

- Python 3.14
- [Poetry](https://python-poetry.org/)
- Docker & Docker Compose (optional, for containerised setup)

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```env
POSTGRES_DB=moodtracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
APP_PORT=5000
FRONTEND_PORT=8501
SWAGGER_PATH=/swagger
```

### Local Development (without Docker)

1. **Install dependencies**

   ```bash
   poetry install --with dev
   ```

2. **Start PostgreSQL** (e.g. via Docker)

   ```bash
   docker run -d --name mood-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:17-alpine
   ```

3. **Run database migrations**

   ```bash
   cd backend
   poetry run alembic upgrade head
   ```

4. **Launch backend**

   ```bash
   poetry run python -m backend.app
   # or
   poetry run uvicorn backend.app.src.app:app --reload --port 5000
   ```

5. **Launch frontend** (in a separate terminal)

   ```bash
   poetry run streamlit run frontend/Home.py --server.port 8501
   ```

### Run with Docker Compose (recommended)

```bash
docker-compose up --build
```

Services will be available at:
- Frontend: `http://localhost:8501`
- Backend API: `http://localhost:5000`
- Swagger docs: `http://localhost:5000/swagger`

## API Endpoints

| Method | Path               | Description                        |
|--------|--------------------|------------------------------------|
| GET    | `/moods`           | List all entries (filter, paginate)|
| POST   | `/moods`           | Create a new mood entry            |
| GET    | `/moods/{id}`      | Retrieve a single entry            |
| DELETE | `/moods/{id}`      | Delete an entry                    |

Full OpenAPI specification is available at `/swagger` or in `docs/openapi.json`.

## Testing

Run unit and integration tests (requires Docker for integration tests):

```bash
cd backend
poetry run pytest tests/ --cov=app.src --cov-fail-under=80
```

Integration tests use `testcontainers` to spin up a temporary PostgreSQL database.

## Code Quality & CI

GitHub Actions run on every pull request and push to `main`/`master`:

- **Lint & Type Check** – Ruff, Black, mypy
- **Code Quality** – radon (complexity), interrogate (docstring coverage)
- **Security** – bandit, pip‑audit
- **Tests** – pytest with coverage (≥80%)

Pre‑commit hooks are configured – install with:

```bash
pre-commit install
```

## Project Structure

```text
.
├── backend/                # FastAPI application
│   ├── app/                # main code (routers, models, settings)
│   ├── alembic/            # database migrations
│   └── tests/              # unit & integration tests
├── frontend/               # Streamlit UI
│   ├── Home.py             # mood logging page
│   ├── pages/Analytics.py  # analytics dashboard
│   └── common.py           # shared UI utilities
├── scripts/                # init‑db.sh
├── docker-compose.yaml
├── pyproject.toml          # dependencies & tool config
└── .env.example
```

## Contributing

1. Fork the repository and create a feature branch.
2. Use [Conventional Commits](https://www.conventionalcommits.org/) for PR titles.
3. Ensure all checks pass (lint, tests, security).
4. Request review from the code owners (see `.github/CODEOWNERS`).

## License

MIT License – see [LICENSE](LICENSE) file for details.
