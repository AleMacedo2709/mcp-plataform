import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path: str) -> str:
    path = file_path.lower()
    try:
        if path.endswith('.pdf'):
            doc = fitz.open(file_path)
            parts = [page.get_text('text') for page in doc]
            return "\n".join(parts)
        if path.endswith('.docx'):
            d = docx.Document(file_path)
            return "\n".join(p.text for p in d.paragraphs)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
            return fh.read()
    except Exception as e:
        return ""
