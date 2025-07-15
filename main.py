from fastapi import FastAPI, File, UploadFile
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
from fastapi import UploadFile, File
from openpyxl import load_workbook
import pandas as pd
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    text = ""
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return {"error": str(e)}

    return {"text": text.strip()}
    
@app.post("/extract-docx")
async def extract_docx(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.docx", "wb") as f:
        f.write(contents)

    doc = Document("temp.docx")
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    
    return {"text": text.strip()}

@app.post("/extract-xlsx")
async def extract_xlsx(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.xlsx", "wb") as f:
        f.write(contents)

    wb = load_workbook("temp.xlsx", read_only=True)
    text_rows = []
    for sheet in wb.worksheets:
        for row in sheet.iter_rows(values_only=True):
            row_text = " ".join(str(cell) for cell in row if cell)
            if row_text.strip():
                text_rows.append(row_text)
    return {"text": "\n".join(text_rows).strip()}

@app.post("/extract-csv")
async def extract_csv(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")
    df = pd.read_csv(StringIO(text), dtype=str)
    combined_text = df.astype(str).fillna("").agg(" ".join, axis=1).tolist()
    
    return {"text": "\n".join(combined_text).strip()}


