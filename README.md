
# File Text Extraction API

A lightweight **FastAPI** service to extract text from multiple file formats — **PDF**, **DOCX**, **XLSX**, and **CSV** — with built-in file size limits, error handling, and CORS support.

## Features
* Extracts text from:
  * **PDF** (via `pdfplumber`)
  * **DOCX** (via `python-docx`)
  * **XLSX** (via `openpyxl`)
  * **CSV** (via Python’s built-in `csv` module)
* Rejects files larger than **5 MB**.
* Returns clean, newline-separated text.
* Cross-Origin Resource Sharing (CORS) enabled for easy integration with frontend apps.

## Tech Stack
* **[FastAPI](https://fastapi.tiangolo.com/)** – API framework
* **[pdfplumber](https://github.com/jsvine/pdfplumber)** – PDF parsing
* **[python-docx](https://python-docx.readthedocs.io/)** – DOCX parsing
* **[openpyxl](https://openpyxl.readthedocs.io/)** – Excel parsing
* **Python csv module** – CSV parsing

## Project Structure
```
file-text-extraction-api/
│
├── main.py          # FastAPI app code
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
```
## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/username/file-text-extraction-api.git
cd file-text-extraction-api
```

**2. Create a virtual environment & activate it:**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```
## Usage
**Run the API locally:**
```bash
uvicorn main:app --reload
The API will start at: http://127.0.0.1:8000
```

## API Endpoints

### **`POST /extract-text`**
Extract text from a PDF file.
* **Body:** `multipart/form-data` with `file` field.
* **Response:** JSON with `"text"` key containing extracted text.

### **`POST /extract-docx`**
Extract text from a DOCX file.

### **`POST /extract-xlsx`**
Extract text from all sheets in an XLSX file.

### **`POST /extract-csv`**
Extract text from a CSV file.

**Example request using `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/extract-docx" \
     -F "file=@sample.docx"
```

## Limitations
* Maximum file size: **5 MB** (configurable in code via `MAX_FILE_SIZE`).
* Only supports UTF-8 encoded CSV files (non-UTF-8 will attempt best-effort decoding).

## 📬 Contact

**Roopali Sharma**: [roopali1193@gmail.com](mailto:roopali1193@gmail.com)

**GitHub**: [@RoopaliS1193](https://github.com/RoopaliS1193)
