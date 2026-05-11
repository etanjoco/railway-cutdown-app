import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "app.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    grade INTEGER,
    bib_number INTEGER UNIQUE,
    score_tech INTEGER DEFAULT 0,
    score_phys INTEGER DEFAULT 0,
    notes TEXT
);
"""


def init_db() -> None:
    """Create the database file and `players` table if they don't exist."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
    finally:
        conn.close()


def get_connection():
    """Return a new SQLite connection (safe to use across threads/processes).

    Callers should close the connection when finished.
    """
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)
