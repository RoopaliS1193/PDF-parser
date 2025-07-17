from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from docx import Document
from openpyxl import load_workbook
from io import BytesIO, StringIO
import csv

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def check_size(contents: bytes, ext: str):
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"{ext.upper()} too large. Max size is 5MB.")

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    check_size(contents, "PDF")

    try:
        with pdfplumber.open(BytesIO(contents)) as pdf:
            text_gen = (page.extract_text() or "" for page in pdf.pages)
            text = "\n".join(filter(None, text_gen))
        return {"text": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

@app.post("/extract-docx")
async def extract_docx(file: UploadFile = File(...)):
    contents = await file.read()
    check_size(contents, "DOCX")

    try:
        doc = Document(BytesIO(contents))
        lines = (p.text.strip() for p in doc.paragraphs if p.text.strip())
        return {"text": "\n".join(lines)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX parsing failed: {str(e)}")

@app.post("/extract-xlsx")
async def extract_xlsx(file: UploadFile = File(...)):
    contents = await file.read()
    check_size(contents, "XLSX")

    try:
        wb = load_workbook(BytesIO(contents), read_only=True)
        def row_text_gen():
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    yield " ".join(str(cell).strip() for cell in row if cell)

        return {"text": "\n".join(row_text_gen())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"XLSX parsing failed: {str(e)}")

@app.post("/extract-csv")
async def extract_csv(file: UploadFile = File(...)):
    contents = await file.read()
    check_size(contents, "CSV")

    try:
        decoded = contents.decode("utf-8", errors="ignore")
        reader = csv.reader(StringIO(decoded))
        lines = (" ".join(cell.strip() for cell in row if cell) for row in reader)
        return {"text": "\n".join(filter(None, lines))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV parsing failed: {str(e)}")
