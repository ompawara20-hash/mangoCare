# MangoCare AI — REST API Documentation

The backend exposes an interactive OpenAPI (Swagger) interface at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

---

## 1. Endpoints

### 1.1 `GET /api/health`
Checks application health, SQLite readiness, active device, and model readiness.

**Example Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_ready": true,
  "disease_model_ready": true,
  "validator_model_ready": true,
  "device": "cpu",
  "operating_mode": "full_inference"
}
```

---

### 1.2 `GET /api/model-info`
Returns verified metadata and provenance for active models.

**Example Response:**
```json
{
  "name": "ixrbhii/mango-disease-convnext",
  "architecture": "ConvNeXt-Small (convnext_small)",
  "input_dimensions": [3, 224, 224],
  "num_classes": 8,
  "supported_classes": [
    "Anthracnose", "Bacterial Canker", "Cutting Weevil",
    "Die Back", "Gall Midge", "Healthy",
    "Powdery Mildew", "Sooty Mould"
  ],
  "target_tissue": "Mango Foliage (Leaves)",
  "evaluation_metrics": {
    "dataset": "MangoLeafBD (Foliar Pathologies)",
    "benchmark_accuracy": "96.4% on held-out test split",
    "license": "Apache 2.0"
  }
}
```

---

### 1.3 `POST /api/analyze`
Accepts a multipart image upload and performs image screening, mango validation, and disease classification.

**Request:**
- `Content-Type: multipart/form-data`
- Body: `file: <binary image file>`

**Example Response (Valid Mango Leaf):**
```json
{
  "success": true,
  "analysis_id": "a91b4c3e-8f2a-4c22-b2d9-110294e772aa",
  "status": "suspected_disease",
  "image_validation": {
    "is_mango": true,
    "status": "accepted",
    "confidence": 0.95
  },
  "prediction": {
    "class_id": "anthracnose",
    "class_name": "Anthracnose",
    "confidence": 0.9421,
    "confidence_category": "high",
    "confidence_interpretation": "High confidence indicating visual symptoms consistent with Anthracnose.",
    "uncertainty_flag": false
  },
  "alternatives": [
    { "class_id": "bacterial_canker", "class_name": "Bacterial Canker", "confidence": 0.0312 }
  ],
  "condition_information": {
    "name": "Anthracnose",
    "scientific_name": "Colletotrichum gloeosporioides",
    "visible_symptoms": ["Small dark-brown or black angular necrotic spots on leaves..."],
    "prevention": ["Prune dead twigs and open the tree canopy..."],
    "management_recommendations": ["Sanitary pruning: cut back infected branch tips..."]
  },
  "report_filename": "MangoCare_Report_a91b4c3e-8f2a-4c22-b2d9-110294e772aa.pdf"
}
```

**Example Response (Non-Mango Image Rejection):**
```json
{
  "success": false,
  "status": "invalid_image",
  "error_code": "MANGO_NOT_DETECTED",
  "message": "The uploaded image does not appear to contain a mango specimen (leaf or fruit).",
  "suggestion": "Please upload a clear photograph of a mango leaf or fruit in natural lighting."
}
```

---

### 1.4 `GET /api/reports/{analysis_id}`
Streams the generated binary PDF assessment report.

**Response Headers:**
- `Content-Type: application/pdf`
- `Content-Disposition: inline; filename=MangoCare_Report_{analysis_id}.pdf`

---

### 1.5 `GET /api/history`
Returns paginated analysis history records.
- Query parameters:
  - `page`: int (default `1`)
  - `page_size`: int (default `10`)
  - `status`: string (optional filter)
  - `search`: string (optional keyword)

---

### 1.6 `DELETE /api/history/{analysis_id}`
Deletes the metadata record from SQLite.

---

### 1.7 `GET /api/statistics`
Returns real-time database counts: total analyses, healthy count, diseased count, inconclusive count, and disease breakdown.

---

### 1.8 `GET /api/diseases` & `GET /api/diseases/{disease_id}`
Returns the comprehensive educational knowledge base records for all supported conditions.
