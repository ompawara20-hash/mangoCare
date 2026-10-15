"""
FastAPI Main Application Entrypoint for MangoCare AI
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.connection import init_db
from app.ml.model_loader import get_model_loader
from app.api.routes import (
    health_router,
    analyze_router,
    reports_router,
    history_router,
    diseases_router
)
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mangocare")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle management."""
    logger.info("Initializing MangoCare AI Database...")
    init_db()

    logger.info("Pre-loading machine learning models...")
    loader = get_model_loader()
    loader.load_all_models()

    logger.info("MangoCare AI Backend is ready to serve requests.")
    yield
    logger.info("MangoCare AI Backend shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-grade automated mango disease detection, foliar pathology screening, "
        "and health assessment system powered by fine-tuned ConvNeXt computer vision models."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_ENV == "development" else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(health_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(diseases_router, prefix="/api")


@app.get("/")
def root_index():
    """Root status indicator and documentation pointers."""
    return {
        "app": "MangoCare AI",
        "description": "Mango Disease Detection & Health Assessment System",
        "status": "online",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "api_endpoints": {
            "health": "/api/health",
            "model_info": "/api/model-info",
            "analyze": "/api/analyze [POST]",
            "history": "/api/history [GET]",
            "statistics": "/api/statistics [GET]",
            "diseases": "/api/diseases [GET]",
            "reports": "/api/reports/{analysis_id} [GET]"
        }
    }


@app.exception_handler(Exception)
async def global_unhandled_exception_handler(request: Request, exc: Exception):
    """Centralized safety handler preventing stack trace leaks to client."""
    logger.error(f"Unhandled system exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred while processing your request.",
            "suggestion": "Please check backend server logs or try again shortly."
        }
    )
