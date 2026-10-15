"""
SQLite Database Connection and Schema Initialization
"""
import sqlite3
from typing import Generator
from app.config import settings
import logging

logger = logging.getLogger(__name__)

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS analyses (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL,
    is_mango INTEGER NOT NULL DEFAULT 1,
    predicted_class_id TEXT,
    predicted_class_name TEXT,
    confidence REAL NOT NULL DEFAULT 0.0,
    confidence_category TEXT NOT NULL DEFAULT 'moderate',
    uncertainty_flag INTEGER NOT NULL DEFAULT 0,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    image_filename TEXT,
    report_filename TEXT,
    top_alternatives_json TEXT,
    symptoms_summary TEXT,
    recommended_action TEXT
);

CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_status ON analyses(status);
CREATE INDEX IF NOT EXISTS idx_analyses_predicted_class ON analyses(predicted_class_id);
"""


def get_db_connection() -> sqlite3.Connection:
    """Creates a new SQLite connection with foreign keys and dict-like row factory."""
    conn = sqlite3.connect(
        settings.DATABASE_PATH,
        timeout=15.0,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def init_db() -> None:
    """Initializes the SQLite database tables and indices."""
    settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db_connection()
    try:
        with conn:
            conn.executescript(CREATE_TABLES_SQL)
        logger.info(f"Database initialized successfully at {settings.DATABASE_PATH}")
    finally:
        conn.close()
