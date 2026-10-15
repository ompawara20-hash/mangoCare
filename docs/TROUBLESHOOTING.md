# MangoCare AI — Troubleshooting Guide

## 1. Common Issues and Resolutions

### Issue 1: Model weights not found (`MODEL_UNAVAILABLE` or `FileNotFoundError`)
- **Cause:** Pretrained weights were not downloaded yet or path is misconfigured.
- **Solution:**
  Run the automated model downloader script:
  ```bash
  python backend/scripts/download_model.py
  ```
  This will download the 98 MB ConvNeXt model and MobileNetV3 validator into `backend/app/ml/weights/`.

---

### Issue 2: Upload fails with `FILE_TOO_LARGE`
- **Cause:** Photograph exceeds the 10 MB upload ceiling.
- **Solution:**
  Resize or compress the image before uploading, or increase `MAX_UPLOAD_SIZE_MB=20` in `.env`.

---

### Issue 3: Image Rejected as `MANGO_NOT_DETECTED`
- **Cause:** The dual-stage validation screener flagged the image as non-botanical (e.g., text document, car, dog, indoor furniture) or monochrome.
- **Solution:**
  Ensure you are uploading a clear photograph of a mango leaf or plant specimen under natural lighting.

---

### Issue 4: ReportLab PDF generation fails
- **Cause:** Missing font or file permission issue in `reports/` folder.
- **Solution:**
  Ensure the `reports/` directory exists and has write permissions. Standard Helvetica is bundled with ReportLab and requires no external fonts.

---

### Issue 5: Port 8000 or 5173 already in use
- **Cause:** Another local service is running on the default ports.
- **Solution:**
  In `.env`, change `BACKEND_PORT=8001` or run frontend with `npm run dev -- --port 5174`.
