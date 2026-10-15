"""
Database Initialization Script
"""
import sys
from pathlib import Path

# Ensure app is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.connection import init_db
from app.config import settings

def main():
    print(f"Initializing SQLite database at: {settings.DATABASE_PATH}")
    init_db()
    print("Database initialization completed successfully.")

if __name__ == "__main__":
    main()
