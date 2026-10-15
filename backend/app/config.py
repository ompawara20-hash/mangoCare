"""
Application Configuration Module for MangoCare AI
"""
from pathlib import Path
import os
from typing import List

# Base Project Paths
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Read .env file manually if present to avoid external dependency issues
def _load_env_file():
    env_candidates = [
        BACKEND_DIR / ".env",
        PROJECT_ROOT / ".env",
    ]
    for env_path in env_candidates:
        if env_path.is_file():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip().strip('"').strip("'")
                            if key not in os.environ:
                                os.environ[key] = val
            except Exception:
                pass
            break

_load_env_file()


class Settings:
    """Central configuration parameters for the MangoCare AI backend."""
    APP_NAME: str = os.getenv("APP_NAME", "MangoCare AI - Mango Disease Detection & Health Assessment System")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # Host & Port
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Uploads & Validation
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    MAX_UPLOAD_BYTES: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = [
        ext.strip().lower() for ext in os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,webp").split(",")
    ]

    # Database
    DATABASE_PATH: Path = (PROJECT_ROOT / "data" / "mangocare.db").resolve()

    # Model Parameters
    WEIGHTS_DIR: Path = (APP_DIR / "ml" / "weights").resolve()
    MANGO_MODEL_ID: str = os.getenv("MANGO_MODEL_ID", "ixrbhii/mango-disease-convnext")
    VALIDATOR_MODEL_NAME: str = os.getenv("VALIDATOR_MODEL_NAME", "mobilenet_v3_small")

    # Decision Thresholds
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.50"))
    HIGH_CONFIDENCE_THRESHOLD: float = float(os.getenv("HIGH_CONFIDENCE_THRESHOLD", "0.70"))
    VALIDATION_THRESHOLD: float = float(os.getenv("VALIDATION_THRESHOLD", "0.60"))

    # Reports
    REPORT_DIR: Path = (PROJECT_ROOT / "reports").resolve()

    # Demo Mode
    ALLOW_DEMO_MODE: bool = os.getenv("ALLOW_DEMO_MODE", "false").lower() in ("true", "1", "yes")

    # Knowledge Base Path
    DISEASE_INFO_PATH: Path = (APP_DIR / "knowledge" / "disease_info.json").resolve()
    LABELS_PATH: Path = (APP_DIR / "ml" / "labels.json").resolve()


settings = Settings()

# Ensure critical runtime directories exist
settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
settings.REPORT_DIR.mkdir(parents=True, exist_ok=True)
settings.WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
