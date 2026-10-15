"""
Image Preprocessing Transformers for Vision Pipelines
"""
import torch
import torchvision.transforms as T
from PIL import Image

# ImageNet Standard Normalization Constants
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# ConvNeXt Mango Disease Classifier Transform
# Input size: 224x224 RGB, normalized to standard mean & std
mango_disease_transform = T.Compose([
    T.Resize((224, 224), interpolation=T.InterpolationMode.BILINEAR),
    T.ToTensor(),
    T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])

# MobileNetV3 Validator Transform
# Standard 256 resize with center crop 224
validator_transform = T.Compose([
    T.Resize(256, interpolation=T.InterpolationMode.BILINEAR),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])


def preprocess_for_classifier(image: Image.Image, device: torch.device) -> torch.Tensor:
    """Applies documented ConvNeXt preprocessing and attaches batch dimension."""
    tensor = mango_disease_transform(image)
    return tensor.unsqueeze(0).to(device)


def preprocess_for_validator(image: Image.Image, device: torch.device) -> torch.Tensor:
    """Applies MobileNetV3 preprocessing and attaches batch dimension."""
    tensor = validator_transform(image)
    return tensor.unsqueeze(0).to(device)
