# Quick Start Guide - EV Battery Health Prediction System

This guide will help you quickly set up and run the complete EV Battery Health Prediction system.

## System Components

1. **Jupyter Notebook** (`battery_health_modeling.ipynb`) - Model training
2. **Flask API** (`app.py`) - Backend API server
3. **Streamlit UI** (`app_ui.py`) - Frontend user interface

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train the Model (First Time Only)

1. Open and run the Jupyter notebook:
   ```bash
   jupyter notebook battery_health_modeling.ipynb
   ```

2. Execute all cells to:
   - Load and preprocess the data
   - Train multiple models (Linear Regression, Random Forest, XGBoost)
   - Evaluate and select the best model
   - Save the model files:
     - `battery_health_model.pkl`
     - `feature_scaler.pkl`
     - `model_info.json`

### Step 3: Start the Flask API Server

Open a terminal and run:

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
```

**Keep this terminal window open!**

### Step 4: Start the Streamlit UI

Open a **new terminal** and run:

```bash
streamlit run app_ui.py
```

The Streamlit app will open automatically in your browser at `http://localhost:8501`

## Using the Application

### In the Streamlit UI:

1. **Adjust Parameters**: Use the sliders in the sidebar to set:
   - Battery Temperature
   - Voltage
   - Current
   - Charging Cycles
   - State of Charge

2. **Predict**: Click the "Predict Battery Health" button

3. **View Results**:
   - Battery health percentage
   - Predicted RUL (Remaining Useful Life)
   - Interactive gauge chart
   - Progress bar
   - Personalized recommendations

4. **Explore Information**:
   - Click on parameter information in the sidebar
   - Read tips and best practices
   - Check health status guide

## File Structure

```
EV-battery-health-prediction/
│
├── data/
│   ├── merged_battery_data.csv
│   └── cleaned_battery_data.csv
│
├── battery_health_modeling.ipynb  # Model training notebook
├── app.py                         # Flask API server
├── app_ui.py                      # Streamlit UI
│
├── battery_health_model.pkl       # Trained model (after training)
├── feature_scaler.pkl             # Feature scaler (after training)
├── model_info.json                # Model metadata (after training)
│
├── requirements.txt               # Python dependencies
├── API_USAGE.md                   # Flask API documentation
├── STREAMLIT_USAGE.md             # Streamlit UI documentation
└── QUICK_START.md                 # This file
```

## Testing

### Test the Flask API:

```bash
python test_api.py
```

### Test the Streamlit UI:

1. Ensure Flask API is running
2. Open Streamlit UI
3. Adjust parameters and click "Predict Battery Health"
4. Verify results are displayed

## Troubleshooting

### Issue: "API Connection Failed" in Streamlit

**Solution**: 
- Ensure Flask API is running (`python app.py`)
- Check that it's running on `http://127.0.0.1:5000`
- Verify model files exist in the project root

### Issue: Model files not found

**Solution**:
- Run the Jupyter notebook to train and save the model
- Ensure `battery_health_model.pkl` and `feature_scaler.pkl` are in the project root

### Issue: Port already in use

**Solution**:
- For Flask: Change port in `app.py` (line 378: `port=5000`)
- For Streamlit: Use `streamlit run app_ui.py --server.port 8502`

### Issue: Missing dependencies

**Solution**:
```bash
pip install -r requirements.txt
```

## API Endpoints

### Flask API (`http://127.0.0.1:5000`)

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Predict battery health

### Streamlit UI (`http://localhost:8501`)

- Main page with input form and results display
- Sidebar with parameter controls and information

## Example Usage

### Using Flask API directly:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "battery_temperature": 32.5,
    "voltage": 3.9,
    "current": 1.2,
    "charging_cycles": 540,
    "state_of_charge": 76
  }'
```

### Using Streamlit UI:

1. Adjust sliders in the sidebar
2. Click "Predict Battery Health"
3. View results and recommendations

## Next Steps

1. **Customize the Model**: Modify hyperparameters in the Jupyter notebook
2. **Add Features**: Extend the API or UI with additional functionality
3. **Deploy**: Deploy the Flask API and Streamlit app to a cloud platform
4. **Monitor**: Add logging and monitoring for production use

## Support

For detailed documentation:
- **API**: See `API_USAGE.md`
- **UI**: See `STREAMLIT_USAGE.md`
- **Model**: See `battery_health_modeling.ipynb`

## Notes

- The model predicts RUL (Remaining Useful Life) in cycles
- Battery health percentage is calculated from RUL
- All predictions are based on the trained machine learning model
- Input validation is performed on both client and server sides

