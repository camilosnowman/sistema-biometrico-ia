import sys
print(f"Testing imports on Python {sys.version}")

try:
    print("Importing pydantic...")
    import pydantic
    print("Pydantic OK")
except Exception as e:
    print(f"Pydantic FAILED: {e}")

try:
    print("Importing fastapi...")
    import fastapi
    print("FastAPI OK")
except Exception as e:
    print(f"FastAPI FAILED: {e}")

try:
    print("Importing PIL (Pillow)...")
    import PIL.Image
    print("Pillow OK")
except Exception as e:
    print(f"Pillow FAILED: {e}")
