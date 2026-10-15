"""
Confidence Scoring, Uncertainty Estimation, and Diagnostic Status Determination
"""
import math
from typing import List, Dict, Any, Tuple
from app.config import settings


def calculate_entropy(probabilities: List[float]) -> float:
    """Computes Shannon entropy across the probability distribution."""
    entropy = 0.0
    for p in probabilities:
        if p > 1e-7:
            entropy -= p * math.log(p)
    return float(entropy)


def evaluate_confidence(
    top_class_name: str,
    top_confidence: float,
    all_probabilities: List[float]
) -> Tuple[str, str, str, bool]:
    """
    Evaluates model confidence and returns:
    - status: 'healthy_appearance_detected' | 'suspected_disease' | 'inconclusive' | 'uncertain_result'
    - confidence_category: 'high' | 'moderate' | 'low'
    - interpretation: educational statement
    - uncertainty_flag: bool
    """
    entropy = calculate_entropy(all_probabilities)
    uncertainty_flag = False

    # Categorize confidence
    if top_confidence >= settings.HIGH_CONFIDENCE_THRESHOLD:
        category = "high"
    elif top_confidence >= settings.CONFIDENCE_THRESHOLD:
        category = "moderate"
    else:
        category = "low"
        uncertainty_flag = True

    # High entropy (> 1.6 out of ln(8) ~ 2.079) indicates the model is divided among multiple conditions
    if entropy > 1.65:
        uncertainty_flag = True

    # Determine clinical/diagnostic status
    is_healthy = (top_class_name.strip().lower() == "healthy")

    if top_confidence < settings.CONFIDENCE_THRESHOLD:
        status = "inconclusive"
        interpretation = (
            f"Low model confidence ({top_confidence:.1%}). The visual features are ambiguous or insufficiently clear. "
            "A sharper, evenly illuminated close-up photograph is strongly advised."
        )
    elif uncertainty_flag:
        status = "uncertain_result"
        if is_healthy:
            interpretation = (
                f"Moderate confidence ({top_confidence:.1%}) of healthy foliage, but elevated model uncertainty was observed. "
                "Monitor the plant and repeat visual screening if symptoms emerge."
            )
        else:
            interpretation = (
                f"Moderate confidence ({top_confidence:.1%}) suggesting possible signs of {top_class_name}. "
                "Due to visual ambiguity, physical verification by a trained agronomist is recommended."
            )
    else:
        if is_healthy:
            status = "healthy_appearance_detected"
            interpretation = (
                f"High confidence ({top_confidence:.1%}) that no typical foliar disease lesions are visible in this specimen. "
                "Note: Latent systemic infections or internal fruit rot cannot be excluded by foliar inspection."
            )
        else:
            status = "suspected_disease"
            interpretation = (
                f"High confidence ({top_confidence:.1%}) indicating visual symptoms consistent with {top_class_name}. "
                "Consult recommended cultural management steps and confirm with local agricultural extension services."
            )

    return status, category, interpretation, uncertainty_flag
