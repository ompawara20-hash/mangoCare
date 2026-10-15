# MangoCare AI - Windows Setup Script (PowerShell)
Write-Host "=============================================" -ForegroundColor Green
Write-Host " MangoCare AI - Automated Setup (Windows)" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# 1. Create Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# 2. Activate Virtual Environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# 3. Install Python Dependencies
Write-Host "Installing backend dependencies..."
pip install -r backend/requirements.txt

# 4. Initialize Database
Write-Host "Initializing SQLite database..."
python backend/scripts/initialize_database.py

# 5. Verify / Download Models
Write-Host "Verifying vision model weights..."
python backend/scripts/download_model.py

# 6. Install Frontend Packages & Build
Write-Host "Installing frontend packages..."
Set-Location frontend
npm install
npm run build
Set-Location ..

Write-Host "=============================================" -ForegroundColor Green
Write-Host " Setup Completed Successfully!" -ForegroundColor Green
Write-Host " Run '.\scripts\run_windows.ps1' to start the app." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Green
