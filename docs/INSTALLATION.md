# MangoCare AI — Installation & Setup Guide

## 1. System Requirements
- **Operating System:** Windows 10/11, macOS (Apple Silicon or Intel), or Linux (Ubuntu 20.04+).
- **Python:** Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Node.js:** Node.js v18.0.0 or higher, with npm 9+.
- **Hardware:** 4 GB RAM minimum (8 GB recommended). Runs inference on CPU or NVIDIA GPU (CUDA).

---

## 2. Setup on Windows (PowerShell)

### Step 1: Extract and Navigate
```powershell
Expand-Archive -Path MangoCare-AI.zip -DestinationPath .
cd MangoCare-AI
```

### Step 2: Set Up Python Backend
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### Step 3: Initialize Database & Verify Weights
```powershell
python backend/scripts/initialize_database.py
python backend/scripts/download_model.py
```

### Step 4: Install Frontend Dependencies
```powershell
cd frontend
npm install
npm run build
cd ..
```

### Step 5: Run Automated Verification Tests
```powershell
python -m pytest backend/tests -v
```

---

## 3. Setup on macOS / Linux (Bash)

```bash
unzip MangoCare-AI.zip
cd MangoCare-AI

# Backend Setup
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Database and Model Initialization
python backend/scripts/initialize_database.py
python backend/scripts/download_model.py

# Frontend Setup
cd frontend
npm install
npm run build
cd ..

# Run Tests
python -m pytest backend/tests -v
```

---

## 4. Running the Application

### Option A: Quick Scripts
- **Windows:** Run `.\scripts\run_windows.ps1`
- **macOS / Linux:** Run `bash ./scripts/run_unix.sh`

### Option B: Manual Separate Terminals
**Terminal 1 (Backend):**
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Open your browser at `http://localhost:5173`.
