"""
Test Machine Learning Inference Pipeline, Tensors, and Confidence Evaluation
"""
import torch
from PIL import Image
from app.ml.preprocessing import preprocess_for_classifier
from app.ml.model_loader import get_model_loader
from app.ml.confidence import evaluate_confidence, calculate_entropy

def test_preprocessing_tensor_shape():
    img = Image.new("RGB", (500, 350), color=(50, 150, 50))
    device = torch.device("cpu")
    tensor = preprocess_for_classifier(img, device)
    assert tensor.shape == torch.Size([1, 3, 224, 224])
    assert tensor.dtype == torch.float32

def test_classifier_prediction_output(fixtures_dir):
    loader = get_model_loader()
    classifier = loader.get_classifier()
    assert classifier.is_ready is True

    img = Image.open(fixtures_dir / "valid_leaf.jpg")
    preds = classifier.predict(img)

    assert len(preds) == 8
    # Check probabilities sum approximately to 1.0
    total_p = sum(p["confidence"] for p in preds)
    assert 0.98 <= total_p <= 1.02

    # Check top prediction structure
    top = preds[0]
    assert "class_id" in top
    assert "class_name" in top
    assert "confidence" in top
    assert top["class_name"] in classifier.labels

def test_confidence_and_entropy_evaluation():
    # Synthetic high confidence
    status, cat, interp, uncertain = evaluate_confidence(
        top_class_name="Healthy",
        top_confidence=0.92,
        all_probabilities=[0.92, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    )
    assert status == "healthy_appearance_detected"
    assert cat == "high"
    assert uncertain is False

    # Synthetic low confidence (inconclusive)
    status_low, cat_low, interp_low, uncertain_low = evaluate_confidence(
        top_class_name="Anthracnose",
        top_confidence=0.35,
        all_probabilities=[0.35, 0.25, 0.20, 0.10, 0.05, 0.02, 0.02, 0.01]
    )
    assert status_low == "inconclusive"
    assert cat_low == "low"
    assert uncertain_low is True
