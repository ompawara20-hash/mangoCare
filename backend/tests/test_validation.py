"""
Test Upload Validation, File Constraints, and Non-Mango Rejection
"""
import pytest
from app.utils.file_validation import validate_upload_file, FileValidationError
from app.utils.image_utils import decode_and_normalize_image, ImageProcessingError

def test_missing_upload_payload(client):
    res = client.post("/api/analyze")
    assert res.status_code == 422  # FastAPI unprocessable entity for missing form field

def test_unsupported_file_extension(client):
    files = {"file": ("malicious.exe", b"MZ\x90\x00\x03\x00\x00\x00", "application/x-msdownload")}
    res = client.post("/api/analyze", files=files)
    assert res.status_code == 400
    detail = res.json()["detail"]
    assert detail["error_code"] == "UNSUPPORTED_EXTENSION"

def test_corrupted_file_content(client, fixtures_dir):
    corrupted_path = fixtures_dir / "corrupted.jpg"
    with open(corrupted_path, "rb") as f:
        files = {"file": ("corrupted.jpg", f.read(), "image/jpeg")}
    res = client.post("/api/analyze", files=files)
    assert res.status_code == 400
    detail = res.json()["detail"]
    assert detail["error_code"] in ("CORRUPTED_FILE_HEADER", "CORRUPTED_IMAGE")

def test_oversized_upload_rejection():
    # 11MB dummy data
    oversized_data = b"\xff\xd8\xff" + b"0" * (11 * 1024 * 1024)
    with pytest.raises(FileValidationError) as exc:
        validate_upload_file("big.jpg", "image/jpeg", oversized_data)
    assert exc.value.error_code == "FILE_TOO_LARGE"

def test_non_mango_document_rejection(client, fixtures_dir):
    doc_path = fixtures_dir / "document.png"
    with open(doc_path, "rb") as f:
        files = {"file": ("invoice.png", f.read(), "image/png")}
    res = client.post("/api/analyze", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is False
    assert data["status"] == "invalid_image"
    assert data["error_code"] == "MANGO_NOT_DETECTED"
    assert "mango" in data["message"].lower() or "document" in data["message"].lower()
