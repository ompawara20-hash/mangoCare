"""
Reproducible Model Evaluation Script
Calculates Top-1 Accuracy, Precision, Recall, Macro F1-Score, and Confusion Matrix
"""
import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ml.model_loader import get_model_loader
from app.config import settings

def evaluate_dataset(dataset_dir: Path):
    print("=" * 65)
    print(" MangoCare AI - Vision Model Evaluation Workflow")
    print("=" * 65)

    if not dataset_dir.is_dir():
        print(f"[ERROR] Evaluation directory not found: {dataset_dir}")
        print("\nExpected directory format:")
        print("  <dataset_dir>/")
        print("    ├── Anthracnose/        (image1.jpg, ...)")
        print("    ├── Bacterial Canker/   (image2.jpg, ...)")
        print("    ├── Healthy/            (image3.jpg, ...)")
        print("    └── ... (all supported classes)")
        print("\nTo evaluate on the MangoLeafBD test split, download the test split from:")
        print("https://huggingface.co/datasets/AfiqN/mango-leaf-disease")
        return

    loader = get_model_loader()
    classifier = loader.get_classifier()
    labels = classifier.labels
    label_to_idx = {name.lower(): idx for idx, name in enumerate(labels)}

    y_true = []
    y_pred = []
    file_count = 0

    print(f"Scanning classes in {dataset_dir}...")
    for class_folder in dataset_dir.iterdir():
        if not class_folder.is_dir():
            continue

        folder_name = class_folder.name.strip().lower()
        matched_idx = None
        for l_name, idx in label_to_idx.items():
            if l_name in folder_name or folder_name in l_name:
                matched_idx = idx
                break

        if matched_idx is None:
            print(f"[SKIP] Folder '{class_folder.name}' does not match supported model classes.")
            continue

        class_images = [
            f for f in class_folder.iterdir()
            if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
        ]
        print(f"Processing '{labels[matched_idx]}': {len(class_images)} images...")

        for img_path in class_images:
            try:
                img = Image.open(img_path).convert("RGB")
                preds = classifier.predict(img)
                top_pred_slug = preds[0]["class_id"]
                top_pred_name = preds[0]["class_name"].lower()

                pred_idx = label_to_idx.get(top_pred_name, 0)
                y_true.append(matched_idx)
                y_pred.append(pred_idx)
                file_count += 1
            except Exception as e:
                print(f"Error reading {img_path}: {e}")

    if file_count == 0:
        print("[WARNING] No valid test images processed.")
        return

    # Calculate metrics
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    total_acc = np.mean(y_true == y_pred)

    print("\n" + "=" * 65)
    print(f" EVALUATION SUMMARY ({file_count} evaluated test samples)")
    print("=" * 65)
    print(f"Overall Top-1 Accuracy: {total_acc:.2%}\n")

    # Per-class metrics
    num_classes = len(labels)
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1

    print(f"{'Class':<22} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Support':<8}")
    print("-" * 65)

    precisions = []
    recalls = []
    f1s = []

    for i in range(num_classes):
        tp = cm[i, i]
        fp = np.sum(cm[:, i]) - tp
        fn = np.sum(cm[i, :]) - tp
        support = np.sum(cm[i, :])

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        if support > 0:
            precisions.append(prec)
            recalls.append(rec)
            f1s.append(f1)
            print(f"{labels[i]:<22} | {prec:<10.2%} | {rec:<10.2%} | {f1:<10.2%} | {support:<8}")

    macro_f1 = np.mean(f1s) if f1s else 0.0
    print("-" * 65)
    print(f"Macro Average F1-Score: {macro_f1:.2%}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Evaluate MangoCare AI model on a test folder.")
    parser.add_argument("--dataset", type=str, default="./data/test_dataset", help="Path to labeled test folder")
    args = parser.parse_args()
    evaluate_dataset(Path(args.dataset))

if __name__ == "__main__":
    main()
