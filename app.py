from flask import Flask, send_file
import io
import os
from pathlib import Path
import zipfile
app = Flask(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent
# Exclude folders/files
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    ".system_generated",
}
EXCLUDE_FILES = {
    "app.py","requirements.txt",  # Current Flask app
}
EXCLUDE_EXTS = {".pyc", ".pyo"}
def create_project_zip():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Exclude directories
            dirs[:] = [
                d for d in dirs
                if d not in EXCLUDE_DIRS
            ]
            for file in files:
                # Exclude specific files
                if file in EXCLUDE_FILES:
                    continue
                # Exclude extensions
                file_path = Path(root) / file
                if file_path.suffix in EXCLUDE_EXTS:
                    continue
                rel_path = file_path.relative_to(PROJECT_ROOT)
                zf.write(
                    file_path,
                    arcname=str(rel_path)
                )
    zip_buffer.seek(0)
    return zip_buffer
@app.route("/")
@app.route("/download")
def download():
    return send_file(
        create_project_zip(),
        mimetype="application/zip",
        as_attachment=True,
        download_name="loan_serve_project.zip"
    )
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

