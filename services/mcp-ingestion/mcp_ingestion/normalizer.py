import os, shutil, uuid
from .document_parser import parse_document_to_text
from .core_settings import RESOURCE_DIR

def normalize_and_store(file_path: str) -> str:
    """Extrai texto e armazena um .txt normalizado em RESOURCE_DIR para RAG."""
    try:
        text = parse_document_to_text(file_path)
        if not text:
            return ""
        os.makedirs(RESOURCE_DIR, exist_ok=True)
        base = os.path.basename(file_path)
        name = os.path.splitext(base)[0] + f"__norm_{uuid.uuid4().hex[:8]}.txt"
        out = os.path.join(RESOURCE_DIR, name)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        return out
    except Exception:
        return ""
