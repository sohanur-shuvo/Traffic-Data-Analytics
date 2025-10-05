#!/usr/bin/env python3
"""
Test script to debug the API comparison endpoint
"""

import requests
import json

# Test the comparison endpoint
def test_comparison():
    url = "http://localhost:5000/api/compare"
    
    # Sample data structure that matches what the frontend sends
    test_data = {
        "data": {
            "success": True,
            "data": [
                {
                    "Date": "2024-01-01",
                    "Time": "08:00:00",
                    "Hour": 8,
                    "Column_4": 10,  # Customer In
                    "Column_5": 5    # Customer Out
                },
                {
                    "Date": "2024-01-01", 
                    "Time": "08:15:00",
                    "Hour": 8,
                    "Column_4": 15,
                    "Column_5": 8
                },
                {
                    "Date": "2024-01-02",
                    "Time": "08:00:00", 
                    "Hour": 8,
                    "Column_4": 12,
                    "Column_5": 6
                },
                {
                    "Date": "2024-01-02",
                    "Time": "08:15:00",
                    "Hour": 8, 
                    "Column_4": 18,
                    "Column_5": 9
                }
            ],
            "available_dates": ["2024-01-01", "2024-01-02"],
            "total_records": 4
        },
        "date1": "2024-01-01",
        "date2": "2024-01-02",
        "show_highlighted_only": False,
        "min_ratio_threshold": 4
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_comparison()
