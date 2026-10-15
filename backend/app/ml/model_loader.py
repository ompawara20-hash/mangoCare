"""
Model Loader Singleton: Lifecycle, Device Detection, and Status Reporting
"""
import torch
import threading
from typing import Optional, Dict, Any
from app.ml.mango_classifier import MangoClassifier
from app.ml.mango_validator import MangoValidator
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """Singleton manager ensuring models are loaded once at startup and reused."""

    _instance: Optional["ModelLoader"] = None
    _lock = threading.Lock()

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Determine optimal inference device
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            logger.info("CUDA detected: Using GPU for accelerated inference.")
        else:
            self.device = torch.device("cpu")
            logger.info("Using CPU for inference.")

        self.classifier: Optional[MangoClassifier] = None
        self.validator: Optional[MangoValidator] = None
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "ModelLoader":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def load_all_models(self):
        """Loads both classifier and validator models."""
        with self._lock:
            if self.classifier is None:
                logger.info("Initializing MangoClassifier...")
                self.classifier = MangoClassifier(self.device)

            if self.validator is None:
                logger.info("Initializing MangoValidator...")
                self.validator = MangoValidator(self.device)

    def get_classifier(self) -> MangoClassifier:
        if self.classifier is None:
            self.load_all_models()
        return self.classifier

    def get_validator(self) -> MangoValidator:
        if self.validator is None:
            self.load_all_models()
        return self.validator

    def get_status(self) -> Dict[str, Any]:
        """Returns readiness and metadata for the health and about endpoints."""
        classifier_ready = self.classifier is not None and self.classifier.is_ready
        validator_ready = self.validator is not None and (self.validator.model is not None or self.validator is not None)

        return {
            "disease_model_ready": classifier_ready,
            "validator_model_ready": validator_ready,
            "device": str(self.device),
            "architecture": "ConvNeXt-Small",
            "model_name": settings.MANGO_MODEL_ID,
            "num_classes": len(self.classifier.labels) if classifier_ready else 8,
            "classes": self.classifier.labels if classifier_ready else [],
            "allow_demo_mode": settings.ALLOW_DEMO_MODE
        }


def get_model_loader() -> ModelLoader:
    return ModelLoader.get_instance()
