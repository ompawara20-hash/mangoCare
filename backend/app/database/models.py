"""
Data models and dataclasses for MangoCare AI persistence
"""
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class AnalysisRecord:
    id: str
    created_at: str
    status: str
    is_mango: bool
    predicted_class_id: Optional[str]
    predicted_class_name: Optional[str]
    confidence: float
    confidence_category: str
    uncertainty_flag: bool
    model_name: str
    model_version: str
    image_filename: Optional[str]
    report_filename: Optional[str]
    top_alternatives_json: str
    symptoms_summary: str
    recommended_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
