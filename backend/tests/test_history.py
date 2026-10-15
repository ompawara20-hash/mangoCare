"""
Test SQLite Persistence, History Pagination, Deletion, and Statistics
"""
import uuid
from datetime import datetime, timezone
from app.database.models import AnalysisRecord
from app.database.repository import AnalysisRepository

def test_database_record_lifecycle():
    repo = AnalysisRepository()
    test_id = str(uuid.uuid4())
    record = AnalysisRecord(
        id=test_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        status="suspected_disease",
        is_mango=True,
        predicted_class_id="anthracnose",
        predicted_class_name="Anthracnose",
        confidence=0.88,
        confidence_category="high",
        uncertainty_flag=False,
        model_name="ConvNeXt-Small",
        model_version="1.0.0",
        image_filename="sample.jpg",
        report_filename=f"MangoCare_Report_{test_id}.pdf",
        top_alternatives_json="[]",
        symptoms_summary="Dark necrotic lesions",
        recommended_action="Pruning and sanitation"
    )

    # 1. Create
    saved = repo.create(record)
    assert saved.id == test_id

    # 2. Retrieve
    retrieved = repo.get_by_id(test_id)
    assert retrieved is not None
    assert retrieved.predicted_class_name == "Anthracnose"
    assert retrieved.confidence == 0.88

    # 3. List
    items, total = repo.list_paginated(page=1, page_size=10)
    assert total >= 1
    assert any(i.id == test_id for i in items)

    # 4. Statistics
    stats = repo.get_statistics()
    assert stats["total_analyses"] >= 1
    assert stats["diseased_count"] >= 1

    # 5. Delete
    deleted = repo.delete_by_id(test_id)
    assert deleted is True
    assert repo.get_by_id(test_id) is None
