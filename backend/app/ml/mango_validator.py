"""
Mango Image Validation and Non-Mango Rejection Module
"""
import torch
import torchvision.models as models
from torchvision.models import MobileNet_V3_Small_Weights
from PIL import Image
import numpy as np
from typing import Tuple, Dict, Any, Optional
from app.ml.preprocessing import preprocess_for_validator
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Keywords in ImageNet class labels that indicate strictly non-agricultural / non-plant categories
REJECTED_IMAGENET_KEYWORDS = {
    # Vehicles & transport
    "car", "cab", "wagon", "truck", "automobile", "motorcycle", "bicycle", "plane", "airplane",
    "boat", "ship", "train", "locomotive", "bus", "jeep", "trailer",
    # Animals & domestic pets
    "dog", "cat", "puppy", "kitten", "retriever", "terrier", "spaniel", "shepherd", "horse", "cow",
    "pig", "sheep", "goat", "elephant", "bear", "tiger", "lion", "wolf", "bird", "fish", "shark",
    # People & clothing
    "person", "man", "woman", "groom", "scuba", "suit", "jersey", "uniform", "sock", "shoe", "hat",
    # Tech & indoor electronics
    "laptop", "computer", "keyboard", "mouse", "monitor", "screen", "cellular", "phone", "television",
    "speaker", "modem", "printer",
    # Structures & furnishings
    "building", "church", "castle", "bridge", "house", "palace", "pillar", "desk", "chair", "sofa",
    "table", "bed", "toilet", "refrigerator",
    # Text, documents & paper
    "envelope", "web site", "website", "packet", "carton", "book jacket", "comic book", "menu",
    "crossword", "newspaper"
}


class MangoValidator:
    """Validates whether an input image plausibly contains a botanical/mango specimen."""

    def __init__(self, device: torch.device):
        self.device = device
        self.model = None
        self.weights = None
        self.categories = []
        self._load_validator_model()

    def _load_validator_model(self):
        try:
            local_weights_path = settings.WEIGHTS_DIR / "mobilenet_v3_small.pth"
            if local_weights_path.is_file():
                self.model = models.mobilenet_v3_small(weights=None)
                state_dict = torch.load(local_weights_path, map_location=self.device, weights_only=True)
                self.model.load_state_dict(state_dict)
                self.weights = MobileNet_V3_Small_Weights.DEFAULT
                self.categories = self.weights.meta.get("categories", [])
            else:
                self.weights = MobileNet_V3_Small_Weights.DEFAULT
                self.model = models.mobilenet_v3_small(weights=self.weights)
                self.categories = self.weights.meta.get("categories", [])

            self.model.to(self.device)
            self.model.eval()
            logger.info("MobileNetV3 validator model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load MobileNetV3 validator weights: {e}. Falling back to spectral heuristics.")
            self.model = None

    def _spectral_foliage_check(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Analyzes color distribution to reject monochrome documents, pure black/white images,
        and completely non-organic chromatic patterns.
        """
        # Downscale to 64x64 for fast statistics
        small = image.resize((64, 64), Image.Resampling.BOX)
        arr = np.array(small, dtype=np.float32)

        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        # Check for near-monochrome images (e.g. printed documents, white paper, receipts)
        rg_diff = np.mean(np.abs(r - g))
        rb_diff = np.mean(np.abs(r - b))
        gb_diff = np.mean(np.abs(g - b))
        total_chromatic_diff = rg_diff + rb_diff + gb_diff

        if total_chromatic_diff < 7.0:
            return False, "The image appears to be a black-and-white or monochrome document rather than organic foliage."

        # Check for presence of typical organic plant hues (green chlorophyll or yellow/brown necrotic pigment)
        # Leaves usually have significant green or warm brown/yellow component
        green_ratio = np.mean(g) / (np.mean(r) + np.mean(g) + np.mean(b) + 1e-5)
        # In rare cases of completely blue or purple artificial lighting:
        blue_dominance = np.mean(b) / (np.mean(r) + np.mean(g) + np.mean(b) + 1e-5)

        if blue_dominance > 0.65 and green_ratio < 0.20:
            return False, "The image lacks organic plant pigmentation (excessive artificial blue lighting or unnatural subject)."

        return True, "Passed spectral check."

    def validate(self, image: Image.Image) -> Dict[str, Any]:
        """
        Runs complete validation pipeline:
        1. Spectral foliage check
        2. MobileNetV3 scene classification
        """
        # Step 1: Spectral / color analysis
        spectral_ok, spectral_reason = self._spectral_foliage_check(image)
        if not spectral_ok:
            return {
                "is_mango": False,
                "status": "invalid_image",
                "error_code": "MANGO_NOT_DETECTED",
                "message": spectral_reason,
                "suggestion": "Please upload a clear photograph of a mango leaf or fruit in natural lighting.",
                "confidence": 0.0,
                "details": {"spectral_passed": False, "top_category": "non_botanical"}
            }

        # Step 2: Deep vision screening (if model is available)
        if self.model is not None and self.categories:
            try:
                input_tensor = preprocess_for_validator(image, self.device)
                with torch.inference_mode():
                    logits = self.model(input_tensor)
                    probs = torch.softmax(logits, dim=-1)[0]

                top_prob, top_idx = torch.topk(probs, k=5)
                top_prob = top_prob.cpu().tolist()
                top_idx = top_idx.cpu().tolist()

                top_class_name = self.categories[top_idx[0]].lower()
                top_score = top_prob[0]

                # Check if top class directly matches rejected non-plant concepts
                for rejected_kw in REJECTED_IMAGENET_KEYWORDS:
                    if rejected_kw in top_class_name and top_score > 0.22:
                        return {
                            "is_mango": False,
                            "status": "invalid_image",
                            "error_code": "MANGO_NOT_DETECTED",
                            "message": f"The image appears to contain an unrelated subject ('{top_class_name}') rather than a mango specimen.",
                            "suggestion": "Please upload a clear, focused photograph of a mango plant specimen (leaf or fruit).",
                            "confidence": float(top_score),
                            "details": {
                                "spectral_passed": True,
                                "top_category": top_class_name,
                                "rejection_keyword": rejected_kw
                            }
                        }

            except Exception as e:
                logger.warning(f"Error during deep validator pass: {e}. Falling back to spectral pass.")

        # If both checks pass:
        return {
            "is_mango": True,
            "status": "accepted",
            "error_code": None,
            "message": "Specimen verified as plausible plant/mango imagery.",
            "suggestion": None,
            "confidence": 0.95,
            "details": {"spectral_passed": True}
        }
