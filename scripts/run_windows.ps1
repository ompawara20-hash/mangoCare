# MangoCare AI - Windows Run Script (PowerShell)
Write-Host "=============================================" -ForegroundColor Green
Write-Host " Starting MangoCare AI Full-Stack System" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Activate virtual environment if present
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
}

# Start Backend in Background Process
Write-Host "Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
$BackendProcess = Start-Process python -ArgumentList "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000" -PassThru

# Start Frontend in Foreground
Write-Host "Launching Frontend on http://localhost:5173..." -ForegroundColor Cyan
Set-Location frontend
try {
    npm run dev
} finally {
    Write-Host "Stopping Backend Server..." -ForegroundColor Yellow
    Stop-Process -Id $BackendProcess.Id -ErrorAction SilentlyContinue
    Set-Location ..
}
