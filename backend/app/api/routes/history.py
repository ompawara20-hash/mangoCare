"""
Analysis History and Statistics Endpoints
"""
import re
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.services.history_service import HistoryService
from app.schemas.analysis import HistoryResponse, HistoryItem, StatisticsResponse

router = APIRouter(tags=["History & Analytics"])
history_service = HistoryService()

UUID_PATTERN = re.compile(r"^[0-9a-fA-F\-]{8,64}$")


@router.get("/history", response_model=HistoryResponse)
def get_analysis_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Optional status filter"),
    search: Optional[str] = Query(None, description="Search by disease or symptom keywords")
):
    """Retrieves paginated historical analysis metadata."""
    return history_service.get_history(
        page=page,
        page_size=page_size,
        status=status,
        search=search
    )


@router.get("/history/{analysis_id}", response_model=HistoryItem)
def get_single_analysis(analysis_id: str):
    """Retrieves metadata for a specific analysis record."""
    if not UUID_PATTERN.match(analysis_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_ID", "message": "Malformed analysis ID."}
        )

    record = history_service.get_record(analysis_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": "Analysis record not found."}
        )

    return record.to_dict()


@router.delete("/history/{analysis_id}")
def delete_analysis_record(analysis_id: str):
    """Deletes an analysis record metadata from SQLite."""
    if not UUID_PATTERN.match(analysis_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_ID", "message": "Malformed analysis ID."}
        )

    success = history_service.delete_record(analysis_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": "Analysis record not found to delete."}
        )

    return {"success": True, "message": f"Analysis {analysis_id} deleted successfully."}


@router.get("/statistics", response_model=StatisticsResponse)
def get_dashboard_statistics():
    """Returns aggregated metrics and counts directly from the SQLite database."""
    return history_service.get_statistics()
