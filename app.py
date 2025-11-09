"""
Flask API for EV Battery Health Prediction

This Flask application provides a REST API endpoint to predict battery health
(RUL - Remaining Useful Life) using a trained machine learning model.
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any, Optional, Tuple

app = Flask(__name__)

# Global variables to store loaded model and scaler
model = None
scaler = None
feature_names = None
feature_medians = None
model_info = None

def load_model_and_scaler():
    """Load the trained model, scaler, and feature information."""
    global model, scaler, feature_names, feature_medians, model_info
    
    try:
        # Load model
        if not os.path.exists('battery_health_model.pkl'):
            raise FileNotFoundError("Model file 'battery_health_model.pkl' not found. Please train the model first.")
        model = joblib.load('battery_health_model.pkl')
        print("✓ Model loaded successfully")
        
        # Load scaler
        if not os.path.exists('feature_scaler.pkl'):
            raise FileNotFoundError("Scaler file 'feature_scaler.pkl' not found. Please train the model first.")
        scaler = joblib.load('feature_scaler.pkl')
        print("✓ Scaler loaded successfully")
        
        # Load model info (contains feature names and metadata)
        if os.path.exists('model_info.json'):
            with open('model_info.json', 'r') as f:
                model_info = json.load(f)
            feature_names = model_info.get('feature_names', [])
            print(f"✓ Model info loaded - {len(feature_names)} features")
        else:
            # If model_info.json doesn't exist, try to infer from dataset
            print("⚠ model_info.json not found. Attempting to infer features from dataset...")
            if os.path.exists('data/merged_battery_data.csv'):
                df = pd.read_csv('data/merged_battery_data.csv', nrows=100)
                exclude_cols = ['RUL', 'Exp_Cell_Type']
                feature_names = [col for col in df.columns 
                               if col not in exclude_cols and df[col].dtype in [np.int64, np.float64]]
                print(f"✓ Inferred {len(feature_names)} features from dataset")
            else:
                raise FileNotFoundError("Cannot determine feature names. Please ensure model_info.json exists or dataset is available.")
        
        # Calculate feature medians from training data for missing features
        if os.path.exists('data/merged_battery_data.csv'):
            df = pd.read_csv('data/merged_battery_data.csv')
            exclude_cols = ['RUL', 'Exp_Cell_Type']
            numeric_cols = [col for col in df.columns 
                          if col not in exclude_cols and df[col].dtype in [np.int64, np.float64]]
            feature_medians = df[numeric_cols].median().to_dict()
            print("✓ Feature medians calculated from dataset")
        else:
            # Use default medians if dataset not available
            feature_medians = {}
            print("⚠ Dataset not found. Using default values for missing features.")
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        raise


def prepare_features(user_input: Dict[str, Any]) -> np.ndarray:
    """
    Convert user input to model features.
    
    Args:
        user_input: Dictionary containing:
            - battery_temperature: float
            - voltage: float
            - current: float
            - charging_cycles: int/float
            - state_of_charge: float (0-100)
    
    Returns:
        numpy array of features ready for model prediction
    """
    # Start with medians/default values for all features
    features = {name: feature_medians.get(name, 0.0) for name in feature_names}
    
    # Map user inputs to model features
    # Direct mappings - check if feature exists in feature_names before assigning
    if 'battery_temperature' in user_input:
        if 'Exp_Temperature' in feature_names:
            features['Exp_Temperature'] = user_input['battery_temperature']
    
    if 'voltage' in user_input:
        voltage = user_input['voltage']
        if 'Exp_Voltage' in feature_names:
            features['Exp_Voltage'] = voltage
        # Use voltage for both max and min voltage if not separately provided
        if 'Max. Voltage Dischar. (V)' in feature_names:
            features['Max. Voltage Dischar. (V)'] = voltage
        if 'Min. Voltage Charg. (V)' in feature_names:
            # Min voltage is typically lower, estimate based on voltage
            features['Min. Voltage Charg. (V)'] = max(voltage - 0.5, 3.0)
    
    if 'current' in user_input:
        if 'Exp_Current' in feature_names:
            features['Exp_Current'] = user_input['current']
    
    if 'charging_cycles' in user_input:
        cycles = float(user_input['charging_cycles'])
        if 'Cycle_Index' in feature_names:
            features['Cycle_Index'] = cycles
        # Calculate cycle_squared if it exists
        if 'cycle_squared' in feature_names:
            features['cycle_squared'] = cycles ** 2
    
    # Calculate derived features if they exist
    if 'voltage_drop' in feature_names:
        if 'Max. Voltage Dischar. (V)' in features and 'Min. Voltage Charg. (V)' in features:
            features['voltage_drop'] = features['Max. Voltage Dischar. (V)'] - features['Min. Voltage Charg. (V)']
    
    if 'energy_density' in feature_names:
        # Estimate energy density (voltage * current * time approximation)
        voltage_val = features.get('Exp_Voltage', features.get('Max. Voltage Dischar. (V)', 3.7))
        current_val = features.get('Exp_Current', 2.0)
        # Use time constant current if available, otherwise estimate
        time_val = features.get('Time constant current (s)', 6000)
        features['energy_density'] = voltage_val * time_val
    
    if 'temp_deviation' in feature_names and 'Exp_Temperature' in features:
        # Calculate temperature deviation (assuming mean temp ~26 based on dataset)
        temp_mean = 26.0  # Approximate mean from dataset
        features['temp_deviation'] = features['Exp_Temperature'] - temp_mean
    
    # Handle state of charge if provided (can estimate some time-based features)
    if 'state_of_charge' in user_input:
        soc = user_input['state_of_charge'] / 100.0  # Convert to 0-1 range
        # Estimate time-based features based on SOC
        # Higher SOC might indicate longer charging time
        if 'Time at 4.15V (s)' in feature_names:
            # Estimate based on SOC (higher SOC = more time at high voltage)
            features['Time at 4.15V (s)'] = 5000 + (soc * 1000)  # Rough estimate
    
    # Estimate Exp_Time based on cycles if not provided
    if 'Exp_Time' in feature_names:
        # Rough estimate: each cycle takes approximately 10000 seconds
        if 'charging_cycles' in user_input:
            cycles = float(user_input['charging_cycles'])
            features['Exp_Time'] = cycles * 10000
    
    # Create feature array in the correct order
    feature_array = np.array([features.get(name, feature_medians.get(name, 0.0)) 
                              for name in feature_names]).reshape(1, -1)
    
    return feature_array


def validate_input(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate user input data.
    
    Args:
        data: Input dictionary to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['battery_temperature', 'voltage', 'current', 'charging_cycles', 'state_of_charge']
    
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate data types and ranges
    try:
        temp = float(data['battery_temperature'])
        if temp < -20 or temp > 60:
            return False, "battery_temperature must be between -20 and 60°C"
        
        voltage = float(data['voltage'])
        if voltage < 2.5 or voltage > 4.5:
            return False, "voltage must be between 2.5 and 4.5V"
        
        current = float(data['current'])
        if current < 0 or current > 10:
            return False, "current must be between 0 and 10A"
        
        cycles = float(data['charging_cycles'])
        if cycles < 0 or cycles > 10000:
            return False, "charging_cycles must be between 0 and 10000"
        
        soc = float(data['state_of_charge'])
        if soc < 0 or soc > 100:
            return False, "state_of_charge must be between 0 and 100"
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid data type: {str(e)}"
    
    return True, None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict battery health (RUL) endpoint.
    
    Expected JSON input:
    {
        "battery_temperature": 32.5,
        "voltage": 3.9,
        "current": 1.2,
        "charging_cycles": 540,
        "state_of_charge": 76
    }
    
    Returns:
    {
        "predicted_rul": 850.5,
        "battery_health_percentage": 76.5,
        "status": "success"
    }
    """
    # Check if model is loaded
    if model is None or scaler is None:
        return jsonify({
            'error': 'Model not loaded. Please ensure model files are available.',
            'status': 'error'
        }), 500
    
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'status': 'error'
            }), 400
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                'error': error_message,
                'status': 'error'
            }), 400
        
        # Prepare features
        try:
            feature_array = prepare_features(data)
        except Exception as e:
            return jsonify({
                'error': f'Error preparing features: {str(e)}',
                'status': 'error'
            }), 500
        
        # Scale features
        try:
            feature_array_scaled = scaler.transform(feature_array)
        except Exception as e:
            return jsonify({
                'error': f'Error scaling features: {str(e)}',
                'status': 'error'
            }), 500
        
        # Make prediction
        try:
            rul_prediction = model.predict(feature_array_scaled)[0]
            # Ensure RUL is non-negative
            rul_prediction = max(0, float(rul_prediction))
        except Exception as e:
            return jsonify({
                'error': f'Error making prediction: {str(e)}',
                'status': 'error'
            }), 500
        
        # Convert RUL to battery health percentage
        # Assuming maximum RUL is around 1200 cycles (based on dataset)
        # Battery health = (current_rul / initial_rul) * 100
        max_rul = 1200  # Approximate maximum RUL from dataset
        battery_health_percentage = min(100, max(0, (rul_prediction / max_rul) * 100))
        
        # Return prediction
        return jsonify({
            'predicted_rul': round(rul_prediction, 2),
            'battery_health_percentage': round(battery_health_percentage, 2),
            'status': 'success',
            'input_data': {
                'battery_temperature': data['battery_temperature'],
                'voltage': data['voltage'],
                'current': data['current'],
                'charging_cycles': data['charging_cycles'],
                'state_of_charge': data['state_of_charge']
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/', methods=['GET'])
def index():
    """API information endpoint."""
    return jsonify({
        'message': 'EV Battery Health Prediction API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /predict': 'Predict battery health (RUL)'
        },
        'example_request': {
            'endpoint': '/predict',
            'method': 'POST',
            'content_type': 'application/json',
            'body': {
                'battery_temperature': 32.5,
                'voltage': 3.9,
                'current': 1.2,
                'charging_cycles': 540,
                'state_of_charge': 76
            }
        }
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("EV Battery Health Prediction API")
    print("=" * 60)
    print("\nLoading model and scaler...")
    
    try:
        load_model_and_scaler()
        print("\n✓ Model and scaler loaded successfully!")
        print("\nStarting Flask server on http://127.0.0.1:5000")
        print("API endpoints:")
        print("  GET  /          - API information")
        print("  GET  /health    - Health check")
        print("  POST /predict   - Predict battery health")
        print("\n" + "=" * 60)
    except Exception as e:
        print(f"\n❌ Failed to load model: {str(e)}")
        print("Please ensure the model files exist and try again.")
        exit(1)
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host=host, port=port, debug=debug)

