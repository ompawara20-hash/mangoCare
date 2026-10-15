"""
Educational Disease Knowledge Base Endpoints
"""
import json
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.config import settings
from app.schemas.analysis import DiseaseListResponse, DiseaseDetailResponse, ConditionInformation

router = APIRouter(tags=["Knowledge Base"])


def _load_all_diseases():
    info_path = settings.DISEASE_INFO_PATH
    if not info_path.is_file():
        return []
    with open(info_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("diseases", [])


@router.get("/diseases", response_model=DiseaseListResponse)
def list_supported_diseases(search: Optional[str] = Query(None, description="Search diseases by keyword")):
    """Returns educational encyclopedia records for all 8 supported mango conditions."""
    diseases = _load_all_diseases()
    if search and search.strip():
        term = search.strip().lower()
        diseases = [
            d for d in diseases
            if term in d.get("name", "").lower()
            or term in d.get("scientific_name", "").lower()
            or term in d.get("description", "").lower()
        ]
    return DiseaseListResponse(diseases=diseases)


@router.get("/diseases/{disease_id}", response_model=DiseaseDetailResponse)
def get_disease_detail(disease_id: str):
    """Returns comprehensive clinical profile for a specific supported mango condition."""
    diseases = _load_all_diseases()
    for d in diseases:
        if d.get("id") == disease_id or d.get("supported_model_class", "").lower() == disease_id.lower():
            return DiseaseDetailResponse(disease=d)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error_code": "DISEASE_NOT_FOUND", "message": f"Disease '{disease_id}' is not in the knowledge base."}
    )
