import os
import sys

print(f"CWD: {os.getcwd()}")
print(f"File: {__file__}")
print(f"Sys Path: {sys.path[:3]}")

app_dir = os.path.dirname(os.path.abspath(__file__))
print(f"App Dir: {app_dir}")

files = os.listdir(app_dir)
print(f"Files in App Dir: {files}")

try:
    import logger
    print("SUCCESS: imported logger")
except Exception as e:
    print(f"FAILURE: could not import logger: {e}")
