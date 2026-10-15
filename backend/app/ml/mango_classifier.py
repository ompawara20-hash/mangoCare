"""
Mango Disease Classifier using Fine-Tuned ConvNeXt Architecture
"""
import json
import torch
import timm
from PIL import Image
from typing import List, Dict, Any, Optional
from pathlib import Path
from app.ml.preprocessing import preprocess_for_classifier
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class MangoClassifier:
    """Performs 8-class disease inference using the verified ConvNeXt-Small checkpoint."""

    def __init__(self, device: torch.device):
        self.device = device
        self.model = None
        self.labels: List[str] = []
        self._load_labels()
        self._load_model()

    def _load_labels(self):
        labels_path = settings.LABELS_PATH
        if not labels_path.is_file():
            # Default fallback labels matching ConvNeXt checkpoint
            self.labels = [
                "Anthracnose", "Bacterial Canker", "Cutting Weevil",
                "Die Back", "Gall Midge", "Healthy",
                "Powdery Mildew", "Sooty Mould"
            ]
        else:
            with open(labels_path, "r", encoding="utf-8") as f:
                self.labels = json.load(f)

    def _load_model(self):
        local_weights = settings.WEIGHTS_DIR / "model.safetensors"
        local_config = settings.WEIGHTS_DIR / "config.json"

        try:
            # 1. First preference: local weights in backend/app/ml/weights
            if local_weights.is_file():
                logger.info(f"Loading ConvNeXt weights from local directory: {local_weights}")
                # Create architecture shell with 8 classes
                self.model = timm.create_model(
                    "convnext_small",
                    num_classes=len(self.labels),
                    pretrained=False
                )
                from safetensors.torch import load_file
                state_dict = load_file(str(local_weights))
                self.model.load_state_dict(state_dict)

            # 2. Second preference: load from HuggingFace Hub or HF Cache
            else:
                logger.info(f"Loading ConvNeXt model from HuggingFace Hub: {settings.MANGO_MODEL_ID}")
                self.model = timm.create_model(
                    f"hf-hub:{settings.MANGO_MODEL_ID}",
                    pretrained=True
                )

            self.model.to(self.device)
            self.model.eval()
            logger.info("MangoClassifier ConvNeXt model successfully initialized.")

        except Exception as e:
            logger.error(f"Failed to load MangoClassifier: {e}")
            self.model = None

    @property
    def is_ready(self) -> bool:
        return self.model is not None

    def predict(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Runs model inference on input PIL Image.
        Returns ranked list of dicts with:
        [
          {"class_id": "anthracnose", "class_name": "Anthracnose", "confidence": 0.942},
          ...
        ]
        """
        if not self.is_ready:
            raise RuntimeError("Mango disease classifier model is not loaded. Cannot run inference.")

        input_tensor = preprocess_for_classifier(image, self.device)

        with torch.inference_mode():
            logits = self.model(input_tensor)
            probs = torch.softmax(logits, dim=-1)[0]

        probs_cpu = probs.cpu().tolist()
        ranked_indices = sorted(range(len(probs_cpu)), key=lambda i: probs_cpu[i], reverse=True)

        results = []
        for idx in ranked_indices:
            name = self.labels[idx] if idx < len(self.labels) else f"Class_{idx}"
            slug = name.strip().lower().replace(" ", "_")
            results.append({
                "class_id": slug,
                "class_name": name,
                "confidence": round(float(probs_cpu[idx]), 4)
            })

        return results
