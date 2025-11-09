# Streamlit UI - Usage Guide

## Overview

The Streamlit UI provides a user-friendly interface for predicting EV battery health. It connects to the Flask API backend to get predictions and displays results with interactive visualizations.

## Prerequisites

1. **Flask API Running**: The Flask API server must be running on `http://127.0.0.1:5000`
   ```bash
   python app.py
   ```

2. **Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Running the Streamlit App

Start the Streamlit application:

```bash
streamlit run app_ui.py
```

The app will open in your default web browser at `http://localhost:8501`

## Features

### 1. Interactive Input Parameters

Use the sidebar to adjust battery parameters:
- **Battery Temperature**: Slider from -20°C to 60°C
- **Voltage**: Slider from 2.5V to 4.5V
- **Current**: Slider from 0A to 10A
- **Charging Cycles**: Slider from 0 to 10,000 cycles
- **State of Charge**: Slider from 0% to 100%

### 2. Prediction Results

Click the "Predict Battery Health" button to:
- Send data to the Flask API
- Receive prediction results
- Display battery health percentage and RUL (Remaining Useful Life)

### 3. Visualizations

- **Gauge Chart**: Interactive gauge showing battery health with color-coded status
- **Progress Bar**: Visual progress bar indicating health percentage
- **Metrics**: Display of predicted RUL and health percentage

### 4. Information & Tips

The app includes:
- **Parameter Information**: Expandable sections explaining each parameter
- **Key Factors**: Important factors affecting battery health
- **Health Status Guide**: Color-coded health status indicators
- **Best Practices**: Tips for maintaining battery health
- **Recommendations**: Personalized recommendations based on input parameters

### 5. Explanatory Text

The app provides helpful explanations:
- Temperature impact on battery degradation
- Voltage indicators for battery performance
- Current draw effects on battery lifespan
- Cycle count implications
- State of charge best practices

## UI Components

### Sidebar
- Input sliders for all battery parameters
- Parameter information and explanations
- Expandable sections with detailed information

### Main Content Area
- Prediction button
- Results display (metrics, gauge, progress bar)
- Recommendations based on inputs
- Input parameter summary

### Information Panel
- Key factors affecting battery health
- Health status guide
- Best practices for battery maintenance

## Color Scheme

- **Primary Color**: Blue (#1f77b4)
- **Background**: White (#ffffff)
- **Secondary Background**: Light Gray (#f0f2f6)
- **Health Status Colors**:
  - Green (80-100%): Excellent
  - Yellow (60-79%): Good
  - Orange (40-59%): Fair
  - Red (0-39%): Poor

## Troubleshooting

### API Connection Error

If you see "API Connection Failed":
1. Ensure Flask API is running: `python app.py`
2. Check that API is on `http://127.0.0.1:5000`
3. Verify model files exist (`battery_health_model.pkl`, `feature_scaler.pkl`)
4. Refresh the Streamlit app

### Port Already in Use

If port 8501 is already in use:
```bash
streamlit run app_ui.py --server.port 8502
```

### Missing Dependencies

Install missing packages:
```bash
pip install -r requirements.txt
```

## Customization

### Theme

Edit `.streamlit/config.toml` to customize:
- Colors
- Font
- Server settings

### Styling

Custom CSS is included in `app_ui.py` for:
- Header styling
- Info boxes
- Warning boxes
- Success boxes
- Progress bars

## Usage Example

1. **Start Flask API**:
   ```bash
   python app.py
   ```

2. **Start Streamlit App** (in another terminal):
   ```bash
   streamlit run app_ui.py
   ```

3. **Use the App**:
   - Adjust parameters using sliders
   - Click "Predict Battery Health"
   - View results and recommendations
   - Explore parameter information in sidebar

## API Integration

The Streamlit app sends POST requests to the Flask API:
- Endpoint: `http://127.0.0.1:5000/predict`
- Method: POST
- Content-Type: application/json
- Response: JSON with prediction results

## Notes

- Predictions are based on the trained machine learning model
- Input validation is performed by the Flask API
- Results are displayed immediately after prediction
- Session state is used to preserve results during interaction
- All visualizations are interactive (using Plotly)

