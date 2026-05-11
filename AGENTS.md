Purpose
Provide short, high-signal notes an automated agent would otherwise miss when working in this repo.

**Quick Start**
- Install dependencies (run from repo root):

```
pip install -r requirements.txt
```

- Run the dev server (this repo uses Hypercorn, not Uvicorn):

```
hypercorn main:app --reload --bind 0.0.0.0:8000
```

- Docker Compose (binds host 8000 -> container 8000, persists DB to ./data):

```
docker compose up --build
docker compose down
```

**ASGI / Entrypoint**
- The FastAPI app object is `main:app`. Always start it with Hypercorn (see commands above) or ensure the server uses that ASGI target.

**Database**
- SQLite DB file path: `data/app.db` (DB directory and file are created by `db.init_db()`).
- There is a DB file present in the repo root (`data/app.db`). Running the app will modify that file. Avoid committing changes to `data/app.db`.
- The FastAPI startup event calls `db.init_db()` automatically when you start Hypercorn; if you run DB-using code outside the server, call `db.init_db()` first.
- To reset the DB locally: stop the server, delete `data/app.db`, then restart (startup recreates the schema).

**CSV import behavior (important for integrations / tests)**
- HTTP endpoint: `POST /players/import` — multipart form field name must be `file`.
- Required CSV header columns: `name` and `grade` (case-insensitive). Example:

```
curl -F "file=@players.csv" http://localhost:8000/players/import
```

- Import semantics: upserts by `name` + `grade`. Empty `grade` is treated as NULL. Invalid rows are skipped and reported.
- Response shape (JSON): `{"processed":N,"inserted":I,"updated":U,"skipped":S,"errors":[...]}`

**Static UI**
- Root `/` serves `static/index.html` (simple frontend that fetches `/players`). Use the web UI to manually verify data.

**Deployment notes**
- Railway/production start command in `railway.json`: `hypercorn main:app --bind "[::]:$PORT"`. Do not hardcode a different port for deployments.
- Dockerfile uses `python:3.11-slim`; prefer matching Python for local reproducibility.

**What this repo does NOT have (so don't look for it)**
- No test suite, no lint/format/typecheck configuration, no CI workflows present in the repository.

Files you will likely need to read first: `README.md`, `main.py`, `db.py`, `csv_import.py`, `docker-compose.yml`, `Dockerfile`, `railway.json`.
