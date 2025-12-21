import os
import sys

# Ensure backend directory is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
backend_dir = os.path.join(project_root, 'backend/app')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.bio_llama_service import llama_service

from PIL import Image
import io

def create_dummy_image():
    """Creates a simple dummy image for testing connectivity (a red square)."""
    img = Image.new('RGB', (320, 240), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def main():
    print("--- Llama 3.2 Vision Connectivity Test ---")
    print(f"Target URL: {llama_service.api_url}")
    print(f"Model: {llama_service.model}")
    
    print("\n[1/2] Generating dummy test image...")
    image_bytes = create_dummy_image()
    print("      (Image generated in memory)")

    print("\n[2/2] Sending to Llama for analysis...")
    print("      (This may take a moment for the first run if model needs to load)")
    
    result = llama_service.analyze_face(image_bytes)
    
    print("\n--- RESULT ---")
    print(result)
    
    if result.emotion == "error":
        print("\n[FAIL] Test Failed.")

        sys.exit(1)
    else:
        print("\n[PASS] Valid JSON received.")

if __name__ == "__main__":
    main()
