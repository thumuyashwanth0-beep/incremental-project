import requests
import zipfile
import io

url = "https://incremental-project-e1q9.onrender.com/"

response = requests.get(url, timeout=60)
response.raise_for_status()

if not response.content.startswith(b"PK"):
    raise ValueError("The URL did not return a ZIP file.")

with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
    zip_file.extractall(".")  # Extract into current working directory

print("Downloaded and extracted successfully.")