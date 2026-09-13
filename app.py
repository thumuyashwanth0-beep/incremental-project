from flask import Flask, send_file
from pathlib import Path
import os

app = Flask(__name__)

# ZIP file in current working directory
ZIP_FILE = Path(__file__).parent / "incremental-project.zip"

@app.route("/")
@app.route("/download")
def download():
    return send_file(
        ZIP_FILE,
        mimetype="application/zip",
        as_attachment=True,
        download_name=ZIP_FILE.name
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )