# EV Battery Health Prediction API - Usage Guide

## Overview

This Flask API provides a REST endpoint to predict battery health (RUL - Remaining Useful Life) using a trained machine learning model.

## Prerequisites

1. **Trained Model Files**: Ensure you have the following files in the project root:
   - `battery_health_model.pkl` - The trained model
   - `feature_scaler.pkl` - The feature scaler
   - `model_info.json` - Model metadata (optional, will be inferred if missing)
   - `data/merged_battery_data.csv` - Dataset for feature inference (optional)

2. **Dependencies**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Starting the Server

Run the Flask application:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API is running and the model is loaded.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
}
```

### 2. API Information

**Endpoint**: `GET /`

**Description**: Get API information and usage examples.

### 3. Predict Battery Health

**Endpoint**: `POST /predict`

**Description**: Predict battery health (RUL) based on input parameters.

**Request Body** (JSON):
```json
{
  "battery_temperature": 32.5,
  "voltage": 3.9,
  "current": 1.2,
  "charging_cycles": 540,
  "state_of_charge": 76
}
```

**Request Parameters**:
- `battery_temperature` (float): Battery temperature in Celsius (range: -20 to 60)
- `voltage` (float): Battery voltage in Volts (range: 2.5 to 4.5)
- `current` (float): Battery current in Amperes (range: 0 to 10)
- `charging_cycles` (int/float): Number of charging cycles (range: 0 to 10000)
- `state_of_charge` (float): State of charge percentage (range: 0 to 100)

**Success Response** (200):
```json
{
  "predicted_rul": 850.5,
  "battery_health_percentage": 76.5,
  "status": "success",
  "input_data": {
    "battery_temperature": 32.5,
    "voltage": 3.9,
    "current": 1.2,
    "charging_cycles": 540,
    "state_of_charge": 76
  }
}
```

**Error Response** (400/500):
```json
{
  "error": "Error message description",
  "status": "error"
}
```

## Usage Examples

### Using cURL

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

### Using Python requests

```python
import requests
import json

url = "http://127.0.0.1:5000/predict"
data = {
    "battery_temperature": 32.5,
    "voltage": 3.9,
    "current": 1.2,
    "charging_cycles": 540,
    "state_of_charge": 76
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (fetch)

```javascript
fetch('http://127.0.0.1:5000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    battery_temperature: 32.5,
    voltage: 3.9,
    current: 1.2,
    charging_cycles: 540,
    state_of_charge: 76
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Testing

A test script is provided to test the API:

```bash
# Make sure the server is running first
python test_api.py
```

## Error Handling

The API includes comprehensive error handling for:

1. **Missing Required Fields**: Returns 400 error with list of missing fields
2. **Invalid Data Types**: Returns 400 error with type information
3. **Out of Range Values**: Returns 400 error with valid range information
4. **Model Loading Errors**: Returns 500 error if model files are missing
5. **Prediction Errors**: Returns 500 error with error details

## Response Fields

- `predicted_rul`: Predicted Remaining Useful Life (in cycles)
- `battery_health_percentage`: Battery health as a percentage (0-100)
- `status`: Request status ("success" or "error")
- `input_data`: Echo of the input data (on success)

## Notes

- The model predicts RUL (Remaining Useful Life) in cycles
- Battery health percentage is calculated as: `(predicted_rul / max_rul) * 100`
- Maximum RUL is assumed to be 1200 cycles (based on training data)
- The API automatically maps user inputs to the model's expected features
- Missing features are filled with median values from the training data

