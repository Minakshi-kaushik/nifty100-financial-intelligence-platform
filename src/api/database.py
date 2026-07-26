"""
database.py

SQLite connection helper for FastAPI.
"""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    """
    Return SQLite connection.
    """
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn
