"""
Pytest Fixtures and Environment Configuration
"""
import sys
import os
import pytest
from pathlib import Path

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# Use isolated test database
os.environ["DATABASE_URL"] = "sqlite:///./data/test_mangocare.db"
os.environ["APP_ENV"] = "test"

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import init_db
from app.config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    settings.DATABASE_PATH = Path("./data/test_mangocare.db").resolve()
    init_db()
    yield
    # Cleanup test db
    if settings.DATABASE_PATH.is_file():
        try:
            settings.DATABASE_PATH.unlink()
        except Exception:
            pass

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"
