from fastapi import FastAPI, UploadFile, File, HTTPException
from app.pdf_utils import extract_text_from_pdf
from app.llm import summarize_cv_with_llm

app = FastAPI(title="Neuram Technical Assessment")

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/summarize-cv")
async def summarize_cv(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()

    cv_text = extract_text_from_pdf(file_bytes)
    if not cv_text:
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

    summary = summarize_cv_with_llm(cv_text)

    if "error" in summary:
        raise HTTPException(status_code=500, detail=summary["error"])

    return summary
