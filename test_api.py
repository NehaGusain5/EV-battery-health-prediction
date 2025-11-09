"""
Test script for the Battery Health Prediction API

This script demonstrates how to use the Flask API to predict battery health.
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:5000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✓ Health check passed\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}\n")
        return False

def test_predict():
    """Test the predict endpoint with sample data."""
    print("Testing /predict endpoint...")
    
    # Sample input data
    sample_data = {
        "battery_temperature": 32.5,
        "voltage": 3.9,
        "current": 1.2,
        "charging_cycles": 540,
        "state_of_charge": 76
    }
    
    print(f"Input data: {json.dumps(sample_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Prediction successful\n")
            return True
        else:
            print(f"❌ Prediction failed\n")
            return False
            
    except Exception as e:
        print(f"❌ Prediction request failed: {str(e)}\n")
        return False

def test_invalid_input():
    """Test the predict endpoint with invalid data."""
    print("Testing /predict endpoint with invalid data...")
    
    # Invalid input (missing required fields)
    invalid_data = {
        "battery_temperature": 32.5,
        "voltage": 3.9
        # Missing current, charging_cycles, state_of_charge
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Error handling working correctly\n")
            return True
        else:
            print(f"⚠ Unexpected status code\n")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}\n")
        return False

def test_out_of_range_values():
    """Test the predict endpoint with out-of-range values."""
    print("Testing /predict endpoint with out-of-range values...")
    
    # Out of range data
    invalid_data = {
        "battery_temperature": 150.0,  # Too high
        "voltage": 3.9,
        "current": 1.2,
        "charging_cycles": 540,
        "state_of_charge": 150  # Too high
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Validation working correctly\n")
            return True
        else:
            print(f"⚠ Unexpected status code\n")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Battery Health Prediction API - Test Script")
    print("=" * 60)
    print("\nMake sure the Flask server is running on http://127.0.0.1:5000")
    print("Start the server with: python app.py\n")
    print("=" * 60)
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health_check()))
    results.append(("Predict (Valid Input)", test_predict()))
    results.append(("Predict (Invalid Input)", test_invalid_input()))
    results.append(("Predict (Out of Range)", test_out_of_range_values()))
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, result in results:
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("=" * 60)

