"""
Image Analysis Endpoint for MangoCare AI
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.analysis_service import AnalysisService
from app.utils.file_validation import FileValidationError
from app.utils.image_utils import ImageProcessingError
from app.schemas.analysis import AnalysisResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Analysis"])
analysis_service = AnalysisService()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_mango_image(file: UploadFile = File(...)):
    """
    Accepts an uploaded photograph of a mango leaf or specimen.
    Performs file integrity checks, non-mango rejection, and ConvNeXt disease classification.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "MISSING_UPLOAD",
                "message": "No file was provided in the upload request.",
                "suggestion": "Please select a valid image file and try again."
            }
        )

    try:
        content = await file.read()
        result = analysis_service.process_image_upload(
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            file_bytes=content
        )
        return result

    except FileValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": e.error_code,
                "message": e.message,
                "suggestion": e.suggestion
            }
        )
    except ImageProcessingError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": e.error_code,
                "message": e.message,
                "suggestion": e.suggestion
            }
        )
    except RuntimeError as e:
        logger.error(f"Inference runtime error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "success": False,
                "error_code": "MODEL_UNAVAILABLE",
                "message": str(e),
                "suggestion": "The AI vision model is currently offline or loading. Please try again shortly."
            }
        )
    except Exception as e:
        logger.exception(f"Unexpected error processing image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "INTERNAL_PROCESSING_ERROR",
                "message": "An unexpected error occurred during image processing.",
                "suggestion": "Please ensure the photograph is clear and properly formatted."
            }
        )
