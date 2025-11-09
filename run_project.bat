@echo off
echo ========================================
echo EV Battery Health Prediction Project
echo ========================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 2: Checking if model files exist...
if exist battery_health_model.pkl (
    echo Model files found!
    goto :start_api
) else (
    echo Model files not found!
    echo You need to train the model first.
    echo.
    echo Please run: jupyter notebook battery_health_modeling.ipynb
    echo Then execute all cells to train the model.
    echo.
    pause
    exit /b 1
)

:start_api
echo.
echo Step 3: Starting Flask API server...
echo Keep this window open!
echo.
start cmd /k "venv\Scripts\activate.bat && python app.py"

timeout /t 3 /nobreak >nul

echo.
echo Step 4: Starting Streamlit UI...
echo.
start cmd /k "venv\Scripts\activate.bat && streamlit run app_ui.py"

echo.
echo ========================================
echo Project started successfully!
echo ========================================
echo.
echo Flask API: http://127.0.0.1:5000
echo Streamlit UI: http://localhost:8501
echo.
echo Press any key to exit this window...
pause >nul

