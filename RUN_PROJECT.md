# How to Run the EV Battery Health Prediction Project

This is a step-by-step guide to run the project on your local machine.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (optional, if cloning from repository)

## Step-by-Step Instructions

### Step 1: Activate Virtual Environment (Recommended)

Since you already have a `venv` folder, activate it:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 2: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (for API)
- Streamlit (for UI)
- Machine Learning libraries (scikit-learn, xgboost)
- Other dependencies

### Step 3: Train the Model (First Time Only)

**IMPORTANT**: You need to train the model before running the API.

#### Option A: Using Jupyter Notebook (Recommended)

1. Start Jupyter Notebook:
   ```bash
   jupyter notebook battery_health_modeling.ipynb
   ```

2. In the notebook:
   - Run all cells (Cell → Run All)
   - Wait for model training to complete
   - This will create:
     - `battery_health_model.pkl`
     - `feature_scaler.pkl`
     - `model_info.json`

#### Option B: Check if Model Files Already Exist

Check if these files exist in your project root:
- `battery_health_model.pkl`
- `feature_scaler.pkl`
- `model_info.json`

If they exist, you can skip training.

### Step 4: Start the Flask API Server

**Open a new terminal window** (keep it running):

```bash
python app.py
```

You should see:
```
============================================================
EV Battery Health Prediction API
============================================================

Loading model and scaler...
✓ Model loaded successfully
✓ Scaler loaded successfully
✓ Model info loaded - X features

✓ Model and scaler loaded successfully!

Starting Flask server on http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

**Keep this terminal window open!** The API server must be running.

### Step 5: Start the Streamlit UI

**Open another terminal window** (or tab):

```bash
streamlit run app_ui.py
```

The Streamlit app will:
1. Start the server
2. Open automatically in your browser at `http://localhost:8501`

If it doesn't open automatically, go to: `http://localhost:8501`

### Step 6: Use the Application

1. **In the Streamlit UI**:
   - Adjust battery parameters using sliders
   - Click "🔮 Predict Battery Health"
   - View results, visualizations, and recommendations
   - Download PDF report (if needed)

2. **Optional: Test the API**:
   - Open a third terminal
   - Run: `python test_api.py`
   - This will test the Flask API endpoints

## Quick Start Commands

Here's a quick reference for running the project:

```bash
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
venv\Scripts\activate.bat    # Windows CMD
# OR
source venv/bin/activate     # Linux/Mac

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Train model (first time only - if files don't exist)
jupyter notebook battery_health_modeling.ipynb

# 4. Start Flask API (Terminal 1)
python app.py

# 5. Start Streamlit UI (Terminal 2)
streamlit run app_ui.py
```

## Troubleshooting

### Issue: "Model file not found"

**Solution**: Train the model first by running the Jupyter notebook.

```bash
jupyter notebook battery_health_modeling.ipynb
```

### Issue: "Port already in use"

**Solution**: 
- For Flask API: Change port in `app.py` or kill the process using port 5000
- For Streamlit: Use different port: `streamlit run app_ui.py --server.port 8502`

### Issue: "Module not found"

**Solution**: Install missing dependencies:

```bash
pip install -r requirements.txt
```

### Issue: "API Connection Failed" in Streamlit

**Solution**: 
1. Make sure Flask API is running (Step 4)
2. Check that it's running on `http://127.0.0.1:5000`
3. Verify model files exist

### Issue: Virtual Environment Not Activating

**Solution**: 
- Windows PowerShell: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Or use CMD instead of PowerShell

## Project Structure

```
EV-battery-health-prediction/
│
├── app.py                          # Flask API server
├── app_ui.py                       # Streamlit UI
├── battery_health_modeling.ipynb   # Model training notebook
│
├── battery_health_model.pkl        # Trained model (after training)
├── feature_scaler.pkl              # Feature scaler (after training)
├── model_info.json                 # Model metadata (after training)
│
├── requirements.txt                # Python dependencies
├── data/                           # Dataset folder
│   └── merged_battery_data.csv
│
└── venv/                           # Virtual environment
```

## What Each Component Does

1. **Flask API (`app.py`)**:
   - Loads the trained model
   - Provides `/predict` endpoint
   - Returns battery health predictions

2. **Streamlit UI (`app_ui.py`)**:
   - User-friendly interface
   - Input sliders for battery parameters
   - Visualizations and charts
   - AI-generated insights
   - PDF report download

3. **Jupyter Notebook (`battery_health_modeling.ipynb`)**:
   - Trains machine learning models
   - Evaluates model performance
   - Saves trained model files

## Next Steps

After running the project:

1. **Make Predictions**: Use the Streamlit UI to predict battery health
2. **Explore Features**: Try different battery parameters
3. **View Reports**: Download PDF reports with predictions
4. **Test API**: Use `test_api.py` to test the API endpoints

## Need Help?

- Check `QUICK_START.md` for detailed setup
- Check `API_USAGE.md` for API documentation
- Check `STREAMLIT_USAGE.md` for UI documentation
- Check `DEPLOYMENT.md` for cloud deployment

## Example Usage

1. **Start Flask API**:
   ```bash
   python app.py
   ```

2. **Start Streamlit** (in another terminal):
   ```bash
   streamlit run app_ui.py
   ```

3. **Use the app**:
   - Open browser to `http://localhost:8501`
   - Adjust parameters
   - Click "Predict Battery Health"
   - View results!

That's it! Your project should now be running. 🚀

