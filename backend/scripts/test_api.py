import requests
import sys

def test_health():
    print("[TEST] Checking /health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Body: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analyze_invalid_type():
    print("\n[TEST] Sending invalid file type to /analyze...")
    try:
        files = {'file': ('test.txt', 'hello world', 'text/plain')}
        response = requests.post("http://localhost:8000/analyze", files=files)
        print(f"Status: {response.status_code} (Expected 400)")
        print(f"Detail: {response.json().get('detail')}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analyze_too_large():
    print("\n[TEST] Sending a 6MB dummy file to /analyze...")
    try:
        # Create a large dummy content
        large_content = b"0" * (6 * 1024 * 1024) 
        files = {'file': ('large.jpg', large_content, 'image/jpeg')}
        response = requests.post("http://localhost:8000/analyze", files=files)
        print(f"Status: {response.status_code} (Expected 413)")
        print(f"Detail: {response.json().get('detail')}")
        return response.status_code == 413
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== API Verification Suite ===\n")
    results = [
        test_health(),
        test_analyze_invalid_type(),
        test_analyze_too_large()
    ]
    
    if all(results):
        print("\n[PASS] All core API validations passed!")
        sys.exit(0)
    else:
        print("\n[FAIL] Some tests failed. Ensure uvicorn is running on port 8000.")
        sys.exit(1)
