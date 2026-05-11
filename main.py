from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from starlette.concurrency import run_in_threadpool
import sqlite3
from pathlib import Path

import db
import csv_import

app = FastAPI()


@app.on_event("startup")
def startup():
    db.init_db()


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the simple frontend UI (static single-file)."""
    html_path = Path(__file__).parent / "static" / "index.html"
    if not html_path.exists():
        return HTMLResponse("<h1>UI not found</h1>", status_code=404)
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/players")
async def get_players():
    """Return all players as JSON."""

    def _query():
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, grade, bib_number, score_tech, score_phys, notes FROM players"
            )
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    players = await run_in_threadpool(_query)
    return players


@app.post("/players/import")
async def import_players(file: UploadFile = File(...)):
    """Accept a CSV file (multipart/form-data) and import players.

    Expects a header with `name` and `grade`. Returns a JSON summary.
    """
    content = await file.read()
    try:
        result = await run_in_threadpool(csv_import.import_players_from_bytes, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result