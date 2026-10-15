"""
End-to-End Inference Pipeline: Validation, Prediction, Confidence, and Knowledge Association
"""
import json
from PIL import Image
from typing import Dict, Any, Optional
from app.ml.model_loader import get_model_loader
from app.ml.confidence import evaluate_confidence
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Cache loaded disease info in memory
_DISEASE_INFO_MAP: Optional[Dict[str, Any]] = None


def _get_disease_knowledge_map() -> Dict[str, Any]:
    global _DISEASE_INFO_MAP
    if _DISEASE_INFO_MAP is not None:
        return _DISEASE_INFO_MAP

    info_path = settings.DISEASE_INFO_PATH
    if not info_path.is_file():
        logger.warning(f"Disease knowledge base file not found at {info_path}")
        return {}

    try:
        with open(info_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            diseases = data.get("diseases", [])
            _DISEASE_INFO_MAP = {d["id"]: d for d in diseases}
            # Also key by supported model class name for easy lookup
            for d in diseases:
                cls_name = d.get("supported_model_class", "").strip().lower()
                if cls_name:
                    _DISEASE_INFO_MAP[cls_name] = d
            return _DISEASE_INFO_MAP
    except Exception as e:
        logger.error(f"Error loading disease knowledge base: {e}")
        return {}


def run_full_inference(image: Image.Image) -> Dict[str, Any]:
    """
    Executes the complete multi-stage ML pipeline:
    1. Mango specimen validation
    2. ConvNeXt disease classification
    3. Uncertainty & confidence scoring
    4. Knowledge base matching
    """
    loader = get_model_loader()
    validator = loader.get_validator()
    classifier = loader.get_classifier()

    # Stage 1: Validation
    validation_res = validator.validate(image)
    if not validation_res["is_mango"]:
        return {
            "success": False,
            "status": "invalid_image",
            "error_code": validation_res["error_code"] or "MANGO_NOT_DETECTED",
            "message": validation_res["message"],
            "suggestion": validation_res["suggestion"],
            "image_validation": validation_res
        }

    # Stage 2: Classifier check
    if not classifier.is_ready:
        if settings.ALLOW_DEMO_MODE:
            logger.warning("Classifier not loaded but DEMO MODE is active. Returning mock demonstration result.")
            return _generate_demo_result(validation_res)
        raise RuntimeError("Disease classification model is offline. Please check weights or internet connection.")

    # Stage 3: Real Disease Classification
    ranked_predictions = classifier.predict(image)
    if not ranked_predictions:
        raise RuntimeError("Model returned empty prediction set.")

    top_pred = ranked_predictions[0]
    all_confs = [p["confidence"] for p in ranked_predictions]

    # Stage 4: Confidence & Uncertainty Evaluation
    status, category, interpretation, uncertainty_flag = evaluate_confidence(
        top_class_name=top_pred["class_name"],
        top_confidence=top_pred["confidence"],
        all_probabilities=all_confs
    )

    # Stage 5: Retrieve Educational Knowledge Base
    knowledge_map = _get_disease_knowledge_map()
    class_slug = top_pred["class_id"]
    class_name_lower = top_pred["class_name"].strip().lower()

    condition_info = knowledge_map.get(class_slug) or knowledge_map.get(class_name_lower) or {
        "id": class_slug,
        "name": top_pred["class_name"],
        "scientific_name": "Mangifera indica condition",
        "category": "foliar",
        "description": "Visual classification indicates features matching this class.",
        "visible_symptoms": ["Visible foliar discoloration or morphological alteration consistent with class."],
        "prevention": ["Routine inspection and adherence to local Good Agricultural Practices (GAP)."],
        "management_recommendations": ["Consult local agricultural extension specialists for guidance."],
        "recommended_next_steps": ["Examine other canopy areas for similar symptoms."],
        "expert_inspection_advised": True,
        "references": ["Local Agricultural Extension Guidelines"],
        "important_limitations": "Preliminary screening result based purely on 2D image."
    }

    # Compile alternatives (excluding the top prediction)
    alternatives = ranked_predictions[1:4]

    return {
        "success": True,
        "status": status,
        "image_validation": validation_res,
        "prediction": {
            "class_id": top_pred["class_id"],
            "class_name": top_pred["class_name"],
            "confidence": top_pred["confidence"],
            "confidence_category": category,
            "confidence_interpretation": interpretation,
            "uncertainty_flag": uncertainty_flag
        },
        "alternatives": alternatives,
        "condition_information": condition_info,
        "model": {
            "name": settings.MANGO_MODEL_ID,
            "architecture": "ConvNeXt-Small",
            "version": "1.0.0 (timm:hf-hub)"
        },
        "limitations": [
            "Image-based foliar screening cannot confirm latent internal fruit rot or fungal presence inside wood vascular bundles.",
            "Visual artifacts, extreme sunlight glare, or pesticide spray deposits may influence classification scores.",
            "Definitive pathogen identification requires laboratory microscopic or PCR confirmation."
        ]
    }


def _generate_demo_result(validation_res: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a strictly labeled mock result when ALLOW_DEMO_MODE=true and weights are absent."""
    return {
        "success": True,
        "status": "suspected_disease",
        "image_validation": validation_res,
        "prediction": {
            "class_id": "anthracnose",
            "class_name": "Anthracnose (DEMO MOCK)",
            "confidence": 0.85,
            "confidence_category": "high",
            "confidence_interpretation": "[DEMO MODE] This is a mock result generated for UI verification without active ML weights.",
            "uncertainty_flag": False
        },
        "alternatives": [
            {"class_id": "bacterial_canker", "class_name": "Bacterial Canker", "confidence": 0.10},
            {"class_id": "healthy", "class_name": "Healthy", "confidence": 0.05}
        ],
        "condition_information": {
            "name": "Anthracnose (DEMO)",
            "scientific_name": "Colletotrichum gloeosporioides",
            "description": "Mock educational record for demonstration purposes.",
            "visible_symptoms": ["Irregular dark lesions"],
            "prevention": ["Pruning and sanitation"],
            "management_recommendations": ["Consult local agricultural officer"]
        },
        "model": {
            "name": "MOCK_DEMO_MODEL",
            "architecture": "Synthetic Demo",
            "version": "0.0.0"
        },
        "limitations": ["DEMO MODE ONLY: DO NOT USE FOR REAL DIAGNOSIS."]
    }
