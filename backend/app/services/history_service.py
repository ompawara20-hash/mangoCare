"""
History Service for managing stored analysis metadata and reports
"""
from typing import Optional, List, Dict, Any, Tuple
from app.database.repository import AnalysisRepository
from app.database.models import AnalysisRecord
import logging

logger = logging.getLogger(__name__)


class HistoryService:
    def __init__(self):
        self.repo = AnalysisRepository()

    def get_history(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        records, total_count = self.repo.list_paginated(
            page=page,
            page_size=page_size,
            status=status,
            search=search
        )
        total_pages = max(1, (total_count + page_size - 1) // page_size)

        return {
            "items": [r.to_dict() for r in records],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }

    def get_record(self, analysis_id: str) -> Optional[AnalysisRecord]:
        return self.repo.get_by_id(analysis_id)

    def delete_record(self, analysis_id: str) -> bool:
        return self.repo.delete_by_id(analysis_id)

    def get_statistics(self) -> Dict[str, Any]:
        return self.repo.get_statistics()
