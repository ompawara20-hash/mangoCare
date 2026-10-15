"""
Full Integration Tests for API Workflow
"""
def test_full_analysis_workflow(client, fixtures_dir):
    leaf_path = fixtures_dir / "valid_leaf.jpg"
    with open(leaf_path, "rb") as f:
        files = {"file": ("test_leaf.jpg", f.read(), "image/jpeg")}

    res = client.post("/api/analyze", files=files)
    assert res.status_code == 200
    data = res.json()

    assert data["success"] is True
    assert "analysis_id" in data
    assert data["status"] in ("healthy_appearance_detected", "suspected_disease", "inconclusive", "uncertain_result")
    assert "prediction" in data
    assert "class_name" in data["prediction"]
    assert "condition_information" in data
    assert "report_filename" in data
    assert data["report_filename"].endswith(".pdf")

    analysis_id = data["analysis_id"]

    # Verify report is downloadable
    rep_res = client.get(f"/api/reports/{analysis_id}")
    assert rep_res.status_code == 200
    assert rep_res.headers["content-type"] == "application/pdf"
    assert rep_res.content.startswith(b"%PDF-")

    # Verify history record is retrievable
    hist_res = client.get(f"/api/history/{analysis_id}")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["id"] == analysis_id

def test_diseases_endpoints(client):
    res = client.get("/api/diseases")
    assert res.status_code == 200
    data = res.json()
    assert len(data["diseases"]) == 8

    # Search for anthracnose
    search_res = client.get("/api/diseases?search=anthracnose")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert len(search_data["diseases"]) >= 1
    assert search_data["diseases"][0]["name"] == "Anthracnose"

    # Detail lookup
    detail_res = client.get("/api/diseases/anthracnose")
    assert detail_res.status_code == 200
    assert detail_res.json()["disease"]["name"] == "Anthracnose"

    # Not found
    nf_res = client.get("/api/diseases/non_existent_disease")
    assert nf_res.status_code == 404
