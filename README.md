# 🔒 ILovePrivacy

> **Automatically redact sensitive information from documents.**  
> Upload a PDF or text file → get it back with names, emails, phone numbers, and SSNs removed.

---

## What This Project Does

ILovePrivacy is a local web application that scans documents for personally identifiable information (PII) and replaces it with labels like `[NAME]`, `[EMAIL]`, and `[SSN]`.

**Example:**

```
Before:  "Dear John Smith, your SSN 123-45-6789 is confirmed."
After:   "Dear █ [NAME], your SSN █ [SSN] is confirmed."
```

No internet connection required. No accounts. No files uploaded to any server. Everything runs on your own computer.

---

## Why I Built This

In financial services and legal industries, teams regularly share documents containing sensitive customer data — often spending hours manually reviewing and redacting information. I built ILovePrivacy to automate this process, inspired by my background working in operations at a large financial institution.

This is my first software project. I built it to learn web development and to solve a real problem I've seen firsthand.

---

## Features

- 📄 **Supports PDF and TXT files**
- 🔍 **Detects 5 types of PII**: Names, email addresses, phone numbers, SSNs, and locations
- 🖥️ **Runs entirely locally** — your files never leave your computer
- ⬇️ **One-click download** of the redacted document
- 🎯 **Drag and drop** file upload
- 🧹 **Auto-deletes** the original uploaded file after processing

---

## Tech Stack

| Layer | Technology | What It Does |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | The page you see in the browser |
| Backend | Python + Flask | Runs the local web server |
| PII Detection | Microsoft Presidio | Finds sensitive information in text |
| PDF Reading | pdfplumber | Extracts text from PDF files |
| PDF Writing | ReportLab | Creates the redacted PDF output |
| Language Model | spaCy (en_core_web_lg) | Understands names and places |

---

## Project Structure

```
iloveprivacy/
│
├── app.py              # Web server — handles file upload and routing
├── redactor.py         # Core logic — finds and replaces PII
├── requirements.txt    # List of Python libraries needed
├── README.md           # This file
│
├── templates/
│   └── index.html      # The web page (UI)
│
├── uploads/            # Temporary storage for uploaded files
└── outputs/            # Redacted files ready to download
```

---

## How to Run It

### Step 1 — Prerequisites
Make sure you have Python installed. Check by running:
```bash
python --version
```
You should see `Python 3.x.x`. If not, download it from [python.org](https://python.org).

### Step 2 — Clone or Download This Project
```bash
git clone https://github.com/yourusername/iloveprivacy.git
cd iloveprivacy
```

### Step 3 — Create a Virtual Environment
```bash
python -m venv venv
```

Activate it:
- **Mac/Linux:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

You'll see `(venv)` at the start of your terminal line. ✅

### Step 4 — Install Libraries
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```
This takes 2–3 minutes. That's normal.

### Step 5 — Run the App
```bash
python app.py
```

### Step 6 — Open in Your Browser
Go to: **http://localhost:5000**

---

## How to Test It

Create a file called `test.txt` with this content:

```
Dear John Smith,
Your application has been reviewed.
SSN: 123-45-6789
Phone: 917-555-1234
Email: john.smith@example.com
Please contact our New York office to confirm.
```

Upload it. You should receive:

```
Dear █ [NAME],
Your application has been reviewed.
SSN: █ [SSN]
Phone: █ [PHONE]
Email: █ [EMAIL]
Please contact our █ [LOCATION] office to confirm.
```

---

## Limitations (Known Issues)

| Limitation | Why | Future Fix |
|---|---|---|
| Scanned PDFs aren't redacted | Scans are images, not text | Add OCR (Tesseract) |
| PDF formatting isn't preserved | Rebuilt as plain text | Use coordinate-based redaction |
| English only | Presidio model is English | Add multilingual models |
| No Word (.docx) support | Not yet implemented | Add python-docx |

---

## What I Learned

- How web servers work (Flask routes, HTTP requests)
- How to handle file uploads safely
- How NLP (Natural Language Processing) identifies names and entities in text
- How PDFs are structured and how to read/write them programmatically
- How to build and run a full-stack web application from scratch

---

## Future Roadmap

- [ ] Add Word document (.docx) support
- [ ] Add OCR for scanned PDFs
- [ ] Show a summary of what was redacted (count by type)
- [ ] Add custom redaction patterns (e.g., internal employee IDs)
- [ ] Deploy to the web with Render or Railway
- [ ] Add Stripe payments for a freemium model

---

## Built With

- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Microsoft Presidio](https://microsoft.github.io/presidio/) — PII detection and anonymization
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [ReportLab](https://www.reportlab.com/) — PDF generation
- [spaCy](https://spacy.io/) — Natural language processing

---

## Author

**Sophia**  
Incoming Process Improvement Analyst - Automations Test Analyst | CCB HL AI Ops & Automation | JPMorganChase  
Building side projects to transition into tech.

---

*This is a portfolio project built for learning purposes. Not intended for production use with real sensitive data without additional security review.*
