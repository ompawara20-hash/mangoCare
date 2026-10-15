"""
Analysis Service orchestrating validation, inference, report generation, and persistence
"""
import uuid
import json
from datetime import datetime
from typing import Dict, Any, Optional

from app.utils.file_validation import validate_upload_file, FileValidationError
from app.utils.image_utils import decode_and_normalize_image, ImageProcessingError
from app.ml.inference import run_full_inference
from app.database.repository import AnalysisRepository
from app.database.models import AnalysisRecord
from app.services.report_service import ReportService
import logging

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self):
        self.repo = AnalysisRepository()
        self.report_service = ReportService()

    def process_image_upload(
        self,
        filename: str,
        content_type: str,
        file_bytes: bytes
    ) -> Dict[str, Any]:
        """
        Coordinates full upload ingestion:
        1. File validation (extension, magic bytes, size)
        2. PIL image decoding and EXIF orientation normalization
        3. Specimen validation (mango vs non-mango) and ConvNeXt disease classification
        4. PDF report generation (for valid analyses)
        5. SQLite persistence of analysis metadata
        """
        # Step 1: File integrity validation
        ext, detected_mime = validate_upload_file(filename, content_type, file_bytes)

        # Step 2: Image decoding and bounding checks
        image, width, height = decode_and_normalize_image(file_bytes)

        # Step 3: ML Vision Inference
        inference_result = run_full_inference(image)

        # Handle non-mango rejection cleanly
        if not inference_result.get("success", False):
            # Do not persist a false disease record; return structured rejection
            return inference_result

        # Step 4: Generate IDs and attach metadata
        analysis_id = str(uuid.uuid4())
        from datetime import timezone
        created_at = datetime.now(timezone.utc).isoformat()

        inference_result["analysis_id"] = analysis_id
        inference_result["created_at"] = created_at
        inference_result["image_metadata"] = {
            "filename": filename,
            "width": width,
            "height": height,
            "format": ext.upper()
        }

        # Step 5: Automatically generate PDF health report
        try:
            pdf_path = self.report_service.generate_pdf_report(inference_result, file_bytes)
            report_filename = pdf_path.name
        except Exception as e:
            logger.error(f"Failed to compile PDF report for {analysis_id}: {e}")
            report_filename = None

        inference_result["report_filename"] = report_filename

        # Step 6: Persist Analysis Record in SQLite Database
        pred = inference_result.get("prediction", {})
        cond = inference_result.get("condition_information", {})
        alts = inference_result.get("alternatives", [])

        symptoms_str = "; ".join(cond.get("visible_symptoms", [])[:3])
        recommended_action_str = cond.get("recommended_next_steps", ["Standard monitoring"])[0] if cond.get("recommended_next_steps") else ""

        record = AnalysisRecord(
            id=analysis_id,
            created_at=created_at,
            status=inference_result.get("status", "unknown"),
            is_mango=True,
            predicted_class_id=pred.get("class_id"),
            predicted_class_name=pred.get("class_name"),
            confidence=pred.get("confidence", 0.0),
            confidence_category=pred.get("confidence_category", "moderate"),
            uncertainty_flag=pred.get("uncertainty_flag", False),
            model_name=inference_result.get("model", {}).get("name", "MangoCare Vision"),
            model_version=inference_result.get("model", {}).get("version", "1.0.0"),
            image_filename=filename,
            report_filename=report_filename,
            top_alternatives_json=json.dumps(alts),
            symptoms_summary=symptoms_str,
            recommended_action=recommended_action_str
        )

        try:
            self.repo.create(record)
            logger.info(f"Persisted analysis {analysis_id} into database successfully.")
        except Exception as e:
            logger.error(f"Database write error for {analysis_id}: {e}")

        return inference_result
