"""
Test PDF Health Report Generation, Content-Type, and Security Constraints
"""
import uuid
from app.services.report_service import ReportService

def test_pdf_report_compilation():
    svc = ReportService()
    test_id = str(uuid.uuid4())

    mock_analysis = {
        "analysis_id": test_id,
        "status": "suspected_disease",
        "prediction": {
            "class_id": "anthracnose",
            "class_name": "Anthracnose",
            "confidence": 0.89,
            "confidence_category": "high",
            "confidence_interpretation": "High probability of foliar anthracnose symptoms."
        },
        "alternatives": [
            {"class_id": "bacterial_canker", "class_name": "Bacterial Canker", "confidence": 0.08}
        ],
        "condition_information": {
            "name": "Anthracnose",
            "scientific_name": "Colletotrichum gloeosporioides",
            "visible_symptoms": ["Dark necrotic spots", "Shot-hole tears on leaves"],
            "prevention": ["Pruning dead twigs", "Adequate spacing"],
            "management_recommendations": ["Sanitary pruning", "Copper fungicide application"]
        },
        "model": {
            "name": "ixrbhii/mango-disease-convnext",
            "architecture": "ConvNeXt-Small"
        }
    }

    pdf_path = svc.generate_pdf_report(mock_analysis)
    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 1000

    # Verify standard PDF magic header
    with open(pdf_path, "rb") as f:
        header = f.read(5)
        assert header == b"%PDF-"

def test_report_endpoint_invalid_id(client):
    res = client.get("/api/reports/not-a-valid-id!!")
    assert res.status_code == 400
    assert res.json()["detail"]["error_code"] == "INVALID_ANALYSIS_ID"

def test_report_endpoint_not_found(client):
    dummy_uuid = str(uuid.uuid4())
    res = client.get(f"/api/reports/{dummy_uuid}")
    assert res.status_code == 404
