"""
Pydantic Models for Analysis Requests and Responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["healthy"])
    version: str = Field(..., examples=["1.0.0"])
    database_ready: bool = Field(..., examples=[True])
    disease_model_ready: bool = Field(..., examples=[True])
    validator_model_ready: bool = Field(..., examples=[True])
    device: str = Field(..., examples=["cpu"])
    operating_mode: str = Field(..., examples=["full_inference"])


class ModelInfoResponse(BaseModel):
    name: str = Field(..., examples=["ixrbhii/mango-disease-convnext"])
    architecture: str = Field(..., examples=["ConvNeXt-Small"])
    input_dimensions: List[int] = Field(default=[3, 224, 224])
    num_classes: int = Field(default=8)
    supported_classes: List[str]
    target_tissue: str = Field(default="Mango Foliage (Leaves)")
    preprocessing_summary: Dict[str, Any]
    evaluation_metrics: Dict[str, Any]
    limitations: List[str]


class ValidationDetail(BaseModel):
    is_mango: bool
    status: str
    error_code: Optional[str] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None
    confidence: Optional[float] = None
    details: Optional[Dict[str, Any]] = None


class PredictionDetail(BaseModel):
    class_id: str
    class_name: str
    confidence: float
    confidence_category: str
    confidence_interpretation: str
    uncertainty_flag: bool


class AlternativePrediction(BaseModel):
    class_id: str
    class_name: str
    confidence: float


class ConditionInformation(BaseModel):
    id: Optional[str] = None
    name: str
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    supported_model_class: Optional[str] = None
    plant_parts_affected: Optional[str] = None
    severity_level: Optional[str] = None
    description: str
    visible_symptoms: List[str] = []
    favorable_conditions: Optional[str] = None
    prevention: List[str] = []
    management_recommendations: List[str] = []
    recommended_next_steps: List[str] = []
    expert_inspection_advised: bool = True
    references: List[str] = []
    important_limitations: Optional[str] = None


class AnalysisResponse(BaseModel):
    success: bool
    analysis_id: Optional[str] = None
    status: str
    error_code: Optional[str] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None
    image_validation: ValidationDetail
    prediction: Optional[PredictionDetail] = None
    alternatives: Optional[List[AlternativePrediction]] = None
    condition_information: Optional[ConditionInformation] = None
    model: Optional[Dict[str, Any]] = None
    limitations: Optional[List[str]] = None
    created_at: Optional[str] = None
    report_filename: Optional[str] = None
    image_metadata: Optional[Dict[str, Any]] = None


class HistoryItem(BaseModel):
    id: str
    created_at: str
    status: str
    is_mango: bool
    predicted_class_id: Optional[str] = None
    predicted_class_name: Optional[str] = None
    confidence: float
    confidence_category: str
    uncertainty_flag: bool
    model_name: str
    model_version: str
    image_filename: Optional[str] = None
    report_filename: Optional[str] = None
    top_alternatives_json: str
    symptoms_summary: str
    recommended_action: str


class PaginationInfo(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    pagination: PaginationInfo


class DiseaseCount(BaseModel):
    name: str
    count: int


class StatisticsResponse(BaseModel):
    total_analyses: int
    healthy_count: int
    diseased_count: int
    inconclusive_count: int
    disease_breakdown: List[DiseaseCount]


class DiseaseDetailResponse(BaseModel):
    disease: ConditionInformation


class DiseaseListResponse(BaseModel):
    diseases: List[ConditionInformation]
