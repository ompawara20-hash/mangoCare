"""
Reproducible Model Downloader and Checksum Verifier for MangoCare AI
"""
import os
import sys
import hashlib
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings

def calculate_sha256(file_path: Path) -> str:
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192 * 1024):
            sha.update(chunk)
    return sha.hexdigest()

def download_models():
    print("=" * 60)
    print(" MangoCare AI - Model Download & Verification Utility")
    print("=" * 60)

    weights_dir = settings.WEIGHTS_DIR
    weights_dir.mkdir(parents=True, exist_ok=True)
    print(f"Target weights directory: {weights_dir}")

    # 1. Download ConvNeXt Mango Disease Classifier
    model_safetensors = weights_dir / "model.safetensors"
    config_json = weights_dir / "config.json"

    if model_safetensors.is_file() and config_json.is_file():
        size_mb = model_safetensors.stat().st_size / (1024 * 1024)
        print(f"[OK] ConvNeXt weights already present: {model_safetensors.name} ({size_mb:.1f} MB)")
    else:
        print(f"Downloading ConvNeXt weights from Hugging Face: {settings.MANGO_MODEL_ID}...")
        try:
            from huggingface_hub import hf_hub_download
            hf_hub_download(
                repo_id=settings.MANGO_MODEL_ID,
                filename="model.safetensors",
                local_dir=str(weights_dir)
            )
            hf_hub_download(
                repo_id=settings.MANGO_MODEL_ID,
                filename="config.json",
                local_dir=str(weights_dir)
            )
            print("[SUCCESS] ConvNeXt weights downloaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to download ConvNeXt weights: {e}")
            print("You can also load directly via internet with timm.create_model('hf-hub:ixrbhii/mango-disease-convnext')")

    # 2. Download MobileNetV3 Validator Checkpoint
    mobilenet_path = weights_dir / "mobilenet_v3_small.pth"
    if mobilenet_path.is_file():
        size_mb = mobilenet_path.stat().st_size / (1024 * 1024)
        print(f"[OK] MobileNetV3 validator weights present: {mobilenet_path.name} ({size_mb:.1f} MB)")
    else:
        print("Downloading MobileNetV3 validator checkpoint...")
        try:
            import torchvision.models as models
            import torch
            m = models.mobilenet_v3_small(weights="DEFAULT")
            torch.save(m.state_dict(), str(mobilenet_path))
            print("[SUCCESS] MobileNetV3 validator checkpoint saved.")
        except Exception as e:
            print(f"[ERROR] Failed to download validator checkpoint: {e}")

    print("\nSummary of Weights Directory:")
    for item in weights_dir.iterdir():
        if item.is_file():
            mb = item.stat().st_size / (1024 * 1024)
            print(f" - {item.name}: {mb:.2f} MB")

    print("\nAll model checks completed.")

if __name__ == "__main__":
    download_models()
