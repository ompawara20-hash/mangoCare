# MangoCare AI — Model Setup & Evaluation Guide

## 1. Checkpoint Overview

MangoCare AI utilizes two vision models:
1. **ConvNeXt-Small (`ixrbhii/mango-disease-convnext`)**:
   - 49.5M parameters, SafeTensors format (98.9 MB).
   - Fine-tuned on the MangoLeafBD benchmark dataset for 8 mango foliar conditions.
   - Licensed under Apache 2.0.
2. **MobileNetV3-Small (`mobilenet_v3_small`)**:
   - 2.5M parameters (9.8 MB).
   - Used for non-mango/non-plant scene screening.

---

## 2. Automated Download Script

To download or verify the checkpoints, run:
```bash
python backend/scripts/download_model.py
```

This verifies the presence of:
- `backend/app/ml/weights/model.safetensors`
- `backend/app/ml/weights/config.json`
- `backend/app/ml/weights/mobilenet_v3_small.pth`

---

## 3. Running Model Evaluation

To evaluate model accuracy, precision, recall, and confusion matrix on a labeled test split:
```bash
python backend/scripts/evaluate_model.py --dataset ./data/test_dataset
```

Expected directory layout:
```
data/test_dataset/
  ├── Anthracnose/
  ├── Bacterial Canker/
  ├── Cutting Weevil/
  ├── Die Back/
  ├── Gall Midge/
  ├── Healthy/
  ├── Powdery Mildew/
  └── Sooty Mould/
```
The script will compute:
- Overall Top-1 Accuracy
- Per-class Precision, Recall, and F1-Score
- Macro Average F1-Score
- Confusion matrix
