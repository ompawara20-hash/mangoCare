"""
API Routes Package for MangoCare AI
"""
from .health import router as health_router
from .analyze import router as analyze_router
from .reports import router as reports_router
from .history import router as history_router
from .diseases import router as diseases_router

__all__ = [
    "health_router",
    "analyze_router",
    "reports_router",
    "history_router",
    "diseases_router"
]
