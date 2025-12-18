import urllib.request
import json

try:
    with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
        data = json.loads(response.read().decode())
        print("Available models:")
        for model in data.get('models', []):
            print(f"- {model['name']}")
except Exception as e:
    print(f"Error listing models: {e}")
