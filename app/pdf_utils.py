import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text content from a PDF file (CV / Resume).

    Args:
        file_bytes (bytes): Raw PDF file in bytes

    Returns:
        str: Extracted text from all pages
    """
    text = ""

    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            text += page.get_text()
    except Exception:
        return ""

    return text.strip()
