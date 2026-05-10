"""
redactor.py — The brain of ILovePrivacy.

What this file does (in plain English):
- Reads your document (PDF or text file)
- Scans every word looking for private information
- Replaces anything sensitive with a label like [NAME] or [SSN]
- Saves a clean version for you to download

Libraries used:
- presidio_analyzer  → finds the sensitive stuff
- presidio_anonymizer → replaces it
- pdfplumber         → reads PDFs
- reportlab          → writes new PDFs
"""

import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


# ---------------------------------------------------------------------------
# Start the engines once when the app loads.
# Think of this like turning on a car — you do it once, not every time
# you want to drive somewhere.
# ---------------------------------------------------------------------------
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# These are the types of private info we look for.
# You can add more later — Presidio supports credit cards, IBANs, and more.
ENTITIES_TO_REDACT = [
    "PERSON",           # Names like "John Smith"
    "EMAIL_ADDRESS",    # Emails like "john@example.com"
    "PHONE_NUMBER",     # Phone numbers like "917-555-1234"
    "US_SSN",           # Social Security Numbers like "123-45-6789"
    "LOCATION",         # Addresses and place names
]

# What we replace each type with
REPLACEMENT_LABELS = {
    "PERSON":        OperatorConfig("replace", {"new_value": "█ [NAME]"}),
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "█ [EMAIL]"}),
    "PHONE_NUMBER":  OperatorConfig("replace", {"new_value": "█ [PHONE]"}),
    "US_SSN":        OperatorConfig("replace", {"new_value": "█ [SSN]"}),
    "LOCATION":      OperatorConfig("replace", {"new_value": "█ [LOCATION]"}),
}


def redact_text(text: str) -> tuple[str, int]:
    """
    Takes a string of text.
    Returns the redacted version + how many things were redacted.

    Example:
        Input:  "Call John Smith at 917-555-1234"
        Output: "Call █ [NAME] at █ [PHONE]", 2
    """
    if not text or not text.strip():
        return text, 0

    # Step 1: Find all the sensitive things
    results = analyzer.analyze(
        text=text,
        entities=ENTITIES_TO_REDACT,
        language="en"
    )

    if not results:
        return text, 0

    # Step 2: Replace them all
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=REPLACEMENT_LABELS
    )

    return anonymized.text, len(results)


def redact_txt(input_path: str, output_path: str) -> dict:
    """
    Redacts a plain .txt file.
    Returns a summary of what happened.
    """
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        original_text = f.read()

    redacted_text, count = redact_text(original_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(redacted_text)

    return {"items_redacted": count, "pages": 1}


def redact_pdf(input_path: str, output_path: str) -> dict:
    """
    Redacts a PDF file page by page.

    How it works:
    1. Open the PDF and read each page's text
    2. Redact the text
    3. Write a brand new PDF with the clean text

    Note for later: This rebuilds the PDF as plain text.
    Fancy formatting (columns, images) won't be preserved — that's fine for v1.
    """
    redacted_pages = []
    total_redacted = 0

    # --- Read the original PDF ---
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()

            if raw_text:
                clean_text, count = redact_text(raw_text)
                redacted_pages.append(clean_text)
                total_redacted += count
            else:
                # Page might be an image/scan — just mark it
                redacted_pages.append("[This page could not be read — it may be a scanned image]")

    # --- Write a new clean PDF ---
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    margin = 50
    line_height = 14
    font_size = 10

    for page_text in redacted_pages:
        # Start writing from the top of the page
        y_position = page_height - margin
        c.setFont("Helvetica", font_size)

        for line in page_text.split("\n"):
            # If we've run out of space, start a new page
            if y_position < margin:
                c.showPage()
                y_position = page_height - margin
                c.setFont("Helvetica", font_size)

            # Write the line
            c.drawString(margin, y_position, line)
            y_position -= line_height

        c.showPage()  # Move to next page

    c.save()

    return {
        "items_redacted": total_redacted,
        "pages": len(redacted_pages)
    }
