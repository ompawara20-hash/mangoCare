"""
Analysis Repository for SQLite Persistence
"""
import json
import sqlite3
from typing import Optional, List, Tuple, Dict, Any
from app.database.connection import get_db_connection
from app.database.models import AnalysisRecord
import logging

logger = logging.getLogger(__name__)


class AnalysisRepository:
    """Repository handling all CRUD and aggregation operations on the analyses table."""

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> AnalysisRecord:
        return AnalysisRecord(
            id=row["id"],
            created_at=row["created_at"],
            status=row["status"],
            is_mango=bool(row["is_mango"]),
            predicted_class_id=row["predicted_class_id"],
            predicted_class_name=row["predicted_class_name"],
            confidence=float(row["confidence"]),
            confidence_category=row["confidence_category"],
            uncertainty_flag=bool(row["uncertainty_flag"]),
            model_name=row["model_name"],
            model_version=row["model_version"],
            image_filename=row["image_filename"],
            report_filename=row["report_filename"],
            top_alternatives_json=row["top_alternatives_json"] or "[]",
            symptoms_summary=row["symptoms_summary"] or "",
            recommended_action=row["recommended_action"] or ""
        )

    def create(self, record: AnalysisRecord) -> AnalysisRecord:
        sql = """
        INSERT INTO analyses (
            id, created_at, status, is_mango, predicted_class_id,
            predicted_class_name, confidence, confidence_category,
            uncertainty_flag, model_name, model_version, image_filename,
            report_filename, top_alternatives_json, symptoms_summary,
            recommended_action
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn = get_db_connection()
        try:
            with conn:
                conn.execute(sql, (
                    record.id,
                    record.created_at,
                    record.status,
                    1 if record.is_mango else 0,
                    record.predicted_class_id,
                    record.predicted_class_name,
                    record.confidence,
                    record.confidence_category,
                    1 if record.uncertainty_flag else 0,
                    record.model_name,
                    record.model_version,
                    record.image_filename,
                    record.report_filename,
                    record.top_alternatives_json,
                    record.symptoms_summary,
                    record.recommended_action
                ))
            return record
        finally:
            conn.close()

    def get_by_id(self, analysis_id: str) -> Optional[AnalysisRecord]:
        sql = "SELECT * FROM analyses WHERE id = ?"
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (analysis_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_record(row)
        finally:
            conn.close()

    def list_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[AnalysisRecord], int]:
        offset = max(0, (page - 1) * page_size)
        conditions = []
        params: List[Any] = []

        if status and status.lower() != "all":
            conditions.append("status = ?")
            params.append(status)

        if search and search.strip():
            conditions.append("(predicted_class_name LIKE ? OR symptoms_summary LIKE ?)")
            pattern = f"%{search.strip()}%"
            params.extend([pattern, pattern])

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        count_sql = f"SELECT COUNT(*) FROM analyses {where_clause}"
        select_sql = f"""
            SELECT * FROM analyses
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """

        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute(count_sql, tuple(params))
            total_count = cur.fetchone()[0]

            select_params = list(params) + [page_size, offset]
            cur.execute(select_sql, tuple(select_params))
            rows = cur.fetchall()

            records = [self._row_to_record(r) for r in rows]
            return records, total_count
        finally:
            conn.close()

    def delete_by_id(self, analysis_id: str) -> bool:
        sql = "DELETE FROM analyses WHERE id = ?"
        conn = get_db_connection()
        try:
            with conn:
                cur = conn.execute(sql, (analysis_id,))
                return cur.rowcount > 0
        finally:
            conn.close()

    def get_statistics(self) -> Dict[str, Any]:
        """Calculates real counts from the database for the dashboard."""
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM analyses")
            total = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM analyses WHERE status = 'healthy_appearance_detected'")
            healthy_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM analyses WHERE status = 'suspected_disease'")
            diseased_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM analyses WHERE status IN ('inconclusive', 'uncertain_result')")
            inconclusive_count = cur.fetchone()[0]

            # Recent disease distribution
            cur.execute("""
                SELECT predicted_class_name, COUNT(*) as cnt
                FROM analyses
                WHERE predicted_class_name IS NOT NULL
                GROUP BY predicted_class_name
                ORDER BY cnt DESC
                LIMIT 6
            """)
            breakdown = [{"name": row[0], "count": row[1]} for row in cur.fetchall()]

            return {
                "total_analyses": total,
                "healthy_count": healthy_count,
                "diseased_count": diseased_count,
                "inconclusive_count": inconclusive_count,
                "disease_breakdown": breakdown
            }
        finally:
            conn.close()
