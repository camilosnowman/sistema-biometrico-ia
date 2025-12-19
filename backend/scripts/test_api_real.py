import requests
from PIL import Image
import io

# Create a simple red image in memory
img = Image.new('RGB', (100, 100), color = 'red')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='JPEG')
img_bytes = img_byte_arr.getvalue()

url = 'http://127.0.0.1:8000/analyze'
files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
