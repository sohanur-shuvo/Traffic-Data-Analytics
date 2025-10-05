#!/usr/bin/env python3
"""
API Connection Test Script
Tests all API endpoints to verify backend is running and accessible
"""
import requests
import sys
import json
from pathlib import Path

API_BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("\n1. Testing Health Check Endpoint...")
    print(f"   GET {API_BASE_URL}/health")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Response: {data}")
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   ❌ Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Cannot connect to {API_BASE_URL}")
        print(f"   ℹ️  Make sure backend server is running: python backend/api.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_upload_endpoint():
    """Test the upload endpoint with a sample request"""
    print("\n2. Testing Upload Endpoint...")
    print(f"   POST {API_BASE_URL}/upload")
    
    # Note: This test just checks if endpoint exists, not actual file upload
    # Actual file upload would require a real Excel file
    
    try:
        # Send empty request to test endpoint availability
        response = requests.post(f"{API_BASE_URL}/upload", timeout=5)
        
        # We expect 400 (no file) rather than 404 (not found)
        if response.status_code == 400:
            print(f"   ✅ Endpoint exists (status: {response.status_code})")
            print(f"   ✅ Expected error: {response.json()}")
            return True
        elif response.status_code == 404:
            print(f"   ❌ Endpoint not found (status: {response.status_code})")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            return True  # Endpoint exists even if behavior is unexpected
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Cannot connect to {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_compare_endpoint():
    """Test the compare endpoint with a sample request"""
    print("\n3. Testing Compare Endpoint...")
    print(f"   POST {API_BASE_URL}/compare")
    
    try:
        # Send minimal request to test endpoint availability
        payload = {
            "excel_data": [],
            "date1": "2024-01-01",
            "date2": "2024-01-02"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/compare",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        # We expect 400 (invalid data) rather than 404 (not found)
        if response.status_code in [200, 400]:
            print(f"   ✅ Endpoint exists (status: {response.status_code})")
            print(f"   ✅ Response: {response.json()}")
            return True
        elif response.status_code == 404:
            print(f"   ❌ Endpoint not found (status: {response.status_code})")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            return True
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Cannot connect to {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_frontend_config():
    """Check if frontend .env file is configured"""
    print("\n4. Checking Frontend Configuration...")
    
    frontend_env = Path(__file__).parent / "frontend" / ".env"
    frontend_env_example = Path(__file__).parent / "frontend" / ".env.example"
    
    if frontend_env.exists():
        print(f"   ✅ .env file exists: {frontend_env}")
        with open(frontend_env, 'r') as f:
            content = f.read()
            if 'VITE_API_BASE_URL' in content:
                print(f"   ✅ VITE_API_BASE_URL is configured")
                return True
            else:
                print(f"   ⚠️  VITE_API_BASE_URL not found in .env")
                return False
    elif frontend_env_example.exists():
        print(f"   ⚠️  .env file not found, but .env.example exists")
        print(f"   ℹ️  Run: python setup-frontend-env.py")
        print(f"   ℹ️  Or copy: cp frontend/.env.example frontend/.env")
        return False
    else:
        print(f"   ⚠️  No .env configuration found")
        print(f"   ℹ️  Run: python setup-frontend-env.py")
        return False

def main():
    """Main test runner"""
    print("=" * 70)
    print("Traffic Analytics Dashboard - API Connection Test")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Upload Endpoint", test_upload_endpoint()))
    results.append(("Compare Endpoint", test_compare_endpoint()))
    results.append(("Frontend Config", check_frontend_config()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    # Overall result
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All tests passed! Your API is ready to use.")
        print("\nNext steps:")
        print("1. Start frontend: cd frontend && npm run dev")
        print("2. Open browser: http://localhost:8080")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure backend is running: python backend/api.py")
        print("2. Configure frontend: python setup-frontend-env.py")
        print("3. See CONFIGURATION.md for detailed setup instructions")
    print("=" * 70)
    
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' module not found")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()

