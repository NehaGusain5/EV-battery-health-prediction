# EV Battery Health Prediction Project - Run Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EV Battery Health Prediction Project" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "Step 1: Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""

# Step 2: Check if model files exist
Write-Host "Step 2: Checking if model files exist..." -ForegroundColor Yellow
if (Test-Path "battery_health_model.pkl") {
    Write-Host "Model files found!" -ForegroundColor Green
} else {
    Write-Host "Model files not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to train the model first." -ForegroundColor Yellow
    Write-Host "Please run: jupyter notebook battery_health_modeling.ipynb" -ForegroundColor Yellow
    Write-Host "Then execute all cells to train the model." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 3: Starting Flask API server..." -ForegroundColor Yellow
Write-Host "Keep the API window open!" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python app.py"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Step 4: Starting Streamlit UI..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; streamlit run app_ui.py"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project started successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Flask API: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Streamlit UI: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"

