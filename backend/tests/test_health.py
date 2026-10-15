"""
Test Health & Model Information Endpoints
"""
def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["app"] == "MangoCare AI"
    assert data["status"] == "online"
    assert "api_endpoints" in data

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "database_ready" in data
    assert data["database_ready"] is True
    assert "disease_model_ready" in data
    assert "device" in data
    assert "operating_mode" in data

def test_model_info_endpoint(client):
    res = client.get("/api/model-info")
    assert res.status_code == 200
    data = res.json()
    assert "ConvNeXt" in data["architecture"]
    assert data["num_classes"] == 8
    assert len(data["supported_classes"]) == 8
    assert "Anthracnose" in data["supported_classes"]
    assert "Healthy" in data["supported_classes"]
    assert "Powdery Mildew" in data["supported_classes"]
    assert "preprocessing_summary" in data
    assert data["input_dimensions"] == [3, 224, 224]
