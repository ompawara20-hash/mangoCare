"""
Pydantic Schemas for MangoCare AI API
"""
from .analysis import (
    HealthResponse,
    ModelInfoResponse,
    AnalysisResponse,
    HistoryResponse,
    StatisticsResponse,
    DiseaseDetailResponse,
    DiseaseListResponse
)

__all__ = [
    "HealthResponse",
    "ModelInfoResponse",
    "AnalysisResponse",
    "HistoryResponse",
    "StatisticsResponse",
    "DiseaseDetailResponse",
    "DiseaseListResponse"
]
