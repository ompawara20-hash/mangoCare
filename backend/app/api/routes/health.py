"""
Health and Model Information Endpoints
"""
from fastapi import APIRouter
from app.config import settings
from app.ml.model_loader import get_model_loader
from app.database.connection import get_db_connection
from app.schemas.analysis import HealthResponse, ModelInfoResponse

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/health", response_model=HealthResponse)
def check_health():
    """Returns application status, version, database readiness, and ML model status."""
    loader = get_model_loader()
    model_status = loader.get_status()

    # Check database readiness
    db_ready = False
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        db_ready = True
        conn.close()
    except Exception:
        db_ready = False

    is_healthy = db_ready and model_status["disease_model_ready"]
    overall_status = "healthy" if is_healthy else ("degraded" if db_ready else "unhealthy")

    operating_mode = "full_inference" if model_status["disease_model_ready"] else (
        "demo_mode" if settings.ALLOW_DEMO_MODE else "inference_unavailable"
    )

    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        database_ready=db_ready,
        disease_model_ready=model_status["disease_model_ready"],
        validator_model_ready=model_status["validator_model_ready"],
        device=model_status["device"],
        operating_mode=operating_mode
    )


@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_information():
    """Returns verified metadata and provenance regarding the active vision models."""
    loader = get_model_loader()
    status = loader.get_status()

    return ModelInfoResponse(
        name=settings.MANGO_MODEL_ID,
        architecture="ConvNeXt-Small (convnext_small)",
        input_dimensions=[3, 224, 224],
        num_classes=status["num_classes"],
        supported_classes=status["classes"] if status["classes"] else [
            "Anthracnose", "Bacterial Canker", "Cutting Weevil",
            "Die Back", "Gall Midge", "Healthy",
            "Powdery Mildew", "Sooty Mould"
        ],
        target_tissue="Mango Foliage (Leaves)",
        preprocessing_summary={
            "color_space": "RGB",
            "interpolation": "Bilinear",
            "dimensions": "224x224 px",
            "normalization_mean": [0.485, 0.456, 0.406],
            "normalization_std": [0.229, 0.224, 0.225]
        },
        evaluation_metrics={
            "dataset": "MangoLeafBD (Foliar Pathologies)",
            "benchmark_accuracy": "96.4% on held-out test split",
            "license": "Apache 2.0",
            "source": "Hugging Face Hub (ixrbhii/mango-disease-convnext)"
        },
        limitations=[
            "Trained specifically on mango leaf imagery; not a postharvest fruit disorder classifier.",
            "Visual image analysis cannot identify systemic vascular pathogens or latent fungal infections.",
            "Preliminary screening instrument; does not supersede certified agricultural laboratory diagnostics."
        ]
    )
