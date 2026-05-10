"""
app.py — The waiter of ILovePrivacy.

What this file does (in plain English):
- Runs a mini web server on your computer
- Listens for someone uploading a file
- Passes the file to redactor.py
- Sends the clean file back to download

To start your app, run this in your terminal:
    python app.py

Then open your browser and go to:
    http://localhost:5000
"""

import os
import uuid
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from redactor import redact_pdf, redact_txt

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Where uploaded files temporarily live
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Maximum file size: 20MB
# (20 * 1024 * 1024 = 20 megabytes in bytes)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

# File types we accept
ALLOWED_EXTENSIONS = {"pdf", "txt"}

# Make sure the folders exist (create them if they don't)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    """
    Checks if the uploaded file is a PDF or TXT.
    We don't want people uploading random things.

    Example:
        allowed_file("report.pdf")  → True
        allowed_file("photo.jpg")   → False
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def unique_filename(original: str) -> str:
    """
    Adds a random ID to filenames so two files called 'report.pdf'
    don't overwrite each other.

    Example:
        unique_filename("report.pdf") → "a3f8b2c1_report.pdf"
    """
    random_prefix = uuid.uuid4().hex[:8]
    return f"{random_prefix}_{secure_filename(original)}"


# ---------------------------------------------------------------------------
# Routes (pages your browser can visit)
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    The home page.
    When you visit http://localhost:5000, this runs
    and shows you the upload page.
    """
    return render_template("index.html")


@app.route("/redact", methods=["POST"])
def redact():
    """
    This runs when you click the 'Redact' button.

    Step by step:
    1. Check that a file was actually uploaded
    2. Check that it's a PDF or TXT
    3. Save it to the uploads/ folder
    4. Run the redactor on it
    5. Send the clean file back
    6. Tell the user how many things were redacted
    """

    # --- Check: did a file arrive? ---
    if "file" not in request.files:
        return jsonify({"error": "No file was uploaded."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "You didn't select a file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and TXT files are supported right now."}), 400

    # --- Save the uploaded file ---
    input_filename = unique_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    file.save(input_path)

    # --- Figure out the file type ---
    extension = input_filename.rsplit(".", 1)[1].lower()

    # --- Name the output file ---
    output_filename = "redacted_" + input_filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # --- Run the redactor ---
    try:
        if extension == "pdf":
            summary = redact_pdf(input_path, output_path)
        elif extension == "txt":
            summary = redact_txt(input_path, output_path)

    except Exception as e:
        # Something went wrong — tell the user in plain English
        return jsonify({
            "error": f"Something went wrong while redacting: {str(e)}"
        }), 500

    # --- Clean up the original uploaded file ---
    # We don't need it anymore — privacy first!
    os.remove(input_path)

    # --- Send the clean file back ---
    return send_file(
        output_path,
        as_attachment=True,
        download_name="redacted_" + secure_filename(file.filename)
    )


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n🔒 ILovePrivacy is running!")
    print("➡  Open your browser and go to: http://localhost:5000\n")
    app.run(debug=True)
