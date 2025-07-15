from fastapi import FastAPI, File, UploadFile
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
