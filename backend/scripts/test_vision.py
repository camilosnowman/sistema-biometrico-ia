import sys
import os
import base64

# Add parent dir to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.services.llama_service import llama_service

def get_dummy_image_bytes():
    """
    Returns bytes of a 1x1 red PNG pixel. 
    Used to verify pipeline without needing PIL/Pillow installed.
    """
    # 1x1 Red PNG Base64
    base64_str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKwAEQAAAABJRU5ErkJggg=="
    return base64.b64decode(base64_str)

def main():
    print("--- Llama 3.2 Vision Connectivity Test (Standard Lib) ---")
    print(f"Target URL: {llama_service.api_url}")
    print(f"Model: {llama_service.model}")
    
    print("\n[1/2] Preparing dummy test image (1x1 px)...")
    image_bytes = get_dummy_image_bytes()
    
    print("\n[2/2] Sending to Llama for analysis...")
    print("      (Asking Llama to analyze a single red pixel - expect 'unknown' or confusion, but valid JSON)")
    
    result = llama_service.analyze_face(image_bytes)
    
    print("\n--- RESULT ---")
    print(result)
    
    if result.get("emotion") == "error":
        print("\n[FAIL] Test Failed.")
        sys.exit(1)
    else:
        print("\n[PASS] Valid JSON received!")
        print("Note: Since we sent a blank red pixel, 'emotion: unknown' is the correct expected behavior.")

if __name__ == "__main__":
    main()
