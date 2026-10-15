"""
PDF Health Assessment Report Download Endpoint
"""
import re
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.services.report_service import ReportService
from app.services.history_service import HistoryService
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Reports"])
report_service = ReportService()
history_service = HistoryService()

UUID_PATTERN = re.compile(r"^[0-9a-fA-F\-]{8,64}$")


@router.get("/reports/{analysis_id}")
def get_pdf_report(analysis_id: str):
    """
    Returns the generated PDF assessment report for a completed analysis.
    Safely validates analysis ID and streams binary application/pdf.
    """
    if not UUID_PATTERN.match(analysis_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "INVALID_ANALYSIS_ID",
                "message": "Malformed analysis identifier format."
            }
        )

    # Check if file exists directly on disk
    pdf_path = report_service.get_report_path(analysis_id)

    # If not on disk, check if record exists in DB to re-generate if needed
    if not pdf_path or not pdf_path.is_file():
        record = history_service.get_record(analysis_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "REPORT_NOT_FOUND",
                    "message": f"No analysis report found for ID '{analysis_id}'."
                }
            )

        # Regenerate report from stored record
        try:
            import json
            alts = []
            try:
                alts = json.loads(record.top_alternatives_json)
            except Exception:
                pass

            mock_payload = {
                "analysis_id": record.id,
                "created_at": record.created_at,
                "status": record.status,
                "prediction": {
                    "class_id": record.predicted_class_id or "healthy",
                    "class_name": record.predicted_class_name or "Healthy Foliage",
                    "confidence": record.confidence,
                    "confidence_category": record.confidence_category,
                    "confidence_interpretation": f"Historical record from {record.created_at}",
                    "uncertainty_flag": record.uncertainty_flag
                },
                "alternatives": alts,
                "condition_information": {
                    "name": record.predicted_class_name or "Mango Specimen",
                    "visible_symptoms": [record.symptoms_summary] if record.symptoms_summary else [],
                    "prevention": ["Consult agricultural guidelines for preventative care."],
                    "management_recommendations": [record.recommended_action] if record.recommended_action else []
                },
                "model": {
                    "name": record.model_name,
                    "architecture": "ConvNeXt-Small",
                    "version": record.model_version
                }
            }
            pdf_path = report_service.generate_pdf_report(mock_payload, image_bytes=None)
        except Exception as e:
            logger.error(f"Error regenerating report: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate PDF report."
            )

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"MangoCare_Report_{analysis_id}.pdf",
        headers={"Content-Disposition": f"inline; filename=MangoCare_Report_{analysis_id}.pdf"}
    )
