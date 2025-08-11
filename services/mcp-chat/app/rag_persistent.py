import os, sqlite3, hashlib, json, time, re
from typing import List, Dict, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    _EMB_MODEL = SentenceTransformer(os.getenv("EMB_MODEL","all-MiniLM-L6-v2"))
except Exception:
    _EMB_MODEL = None

try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None

INDEX_DIR = os.getenv("RAG_INDEX_DIR", "/data/resources/.index")
os.makedirs(INDEX_DIR, exist_ok=True)

DB_PATH = os.path.join(INDEX_DIR, "index.sqlite")
VEC_PATH = os.path.join(INDEX_DIR, "vectors.npy")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS docs (
  id INTEGER PRIMARY KEY,
  file TEXT NOT NULL,
  chunk_start INTEGER NOT NULL,
  chunk_end INTEGER NOT NULL,
  mtime REAL NOT NULL,
  sha256 TEXT NOT NULL,
  text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_file ON docs(file);
CREATE INDEX IF NOT EXISTS idx_sha ON docs(sha256);
"""

def _sha256(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8","ignore")).hexdigest()

def _chunks(text, size=800, overlap=100):
    for i in range(0, max(len(text)-1,0), max(size-overlap,1)):
        yield i, i+size, text[i:i+size]

def _normalize_text(txt: str) -> str:
    return re.sub(r"\s+", " ", txt).strip()

def _open_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    for stmt in SCHEMA_SQL.strip().split(";"):
        if stmt.strip():
            conn.execute(stmt)
    return conn

def _scan_files(root: str) -> List[str]:
    paths = []
    for base, _dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".txt",".md",".csv",".pdf",".docx")):
                paths.append(os.path.join(base,f))
    return paths

def _extract_text(path: str) -> str:
    try:
        if path.lower().endswith(".pdf"):
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(path)
                blocks = []
                for p in doc:
                    blocks.append(p.get_text("text"))
                return "\n".join(blocks)
            except Exception:
                pass
        if path.lower().endswith(".docx"):
            try:
                import docx
                d = docx.Document(path)
                return "\n".join([p.text for p in d.paragraphs])
            except Exception:
                pass
        # txt/md/csv default
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except Exception:
        return ""
    return ""

def build_persistent_index(resource_root: str) -> Dict[str,str]:
    conn = _open_db()
    cur = conn.cursor()
    indexed = 0
    updated = 0
    files = _scan_files(resource_root)
    for path in files:
        try:
            mtime = os.path.getmtime(path)
            text = _normalize_text(_extract_text(path))
            if not text:
                continue
            sha = _sha256(text[:10000])  # barato
            # verificar se já existe entrada com mesmo file e sha
            row = cur.execute("SELECT sha256, mtime FROM docs WHERE file=? ORDER BY id DESC LIMIT 1", (path,)).fetchone()
            if row and row[0] == sha and abs(row[1]-mtime) < 1e-6:
                continue  # sem mudanças
            # remove antigos para este arquivo
            cur.execute("DELETE FROM docs WHERE file=?", (path,))
            # reindexa chunks
            for start, end, chunk in _chunks(text):
                cur.execute(
                    "INSERT INTO docs(file, chunk_start, chunk_end, mtime, sha256, text) VALUES(?,?,?,?,?,?)",
                    (path, start, end, mtime, sha, chunk)
                )
            updated += 1
        except Exception:
            continue
    conn.commit()
    # construir vetores
    if _EMB_MODEL:
        rows = cur.execute("SELECT id, text FROM docs ORDER BY id").fetchall()
        if rows:
            vecs = _EMB_MODEL.encode([r[1] for r in rows], convert_to_numpy=True, normalize_embeddings=True)
            np.save(VEC_PATH, vecs)
    conn.close()
    return {"files": str(len(files)), "updated": str(updated)}

def _highlight(snippet: str, query: str) -> str:
    terms = [re.escape(t) for t in query.lower().split() if len(t) > 2]
    if not terms:
        return snippet[:600]
    pat = re.compile(r'(' + '|'.join(terms) + r')', re.I)
    return pat.sub(lambda m: f"**{m.group(0)}**", snippet)[:800]

def search_hybrid(query: str, top_k: int = 5) -> List[Dict[str,str]]:
    conn = _open_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, file, text FROM docs ORDER BY id").fetchall()
    if not rows:
        conn.close()
        return []
    ids = [r[0] for r in rows]
    files = [r[1] for r in rows]
    texts = [r[2] for r in rows]

    # Embedding similarity
    emb_scores = np.zeros(len(texts))
    if _EMB_MODEL and os.path.exists(VEC_PATH):
        vecs = np.load(VEC_PATH)
        qv = _EMB_MODEL.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        emb_scores = vecs @ qv

    # BM25 (token-based)
    bm25_scores = np.zeros(len(texts))
    if BM25Okapi:
        tokenized = [t.split() for t in texts]
        bm = BM25Okapi(tokenized)
        bm_scores = bm.get_scores(query.split())
        bm25_scores = np.array(bm_scores)

    # Combine (normalize then weighted)
    def _norm(x):
        if x.std() < 1e-9:
            return np.zeros_like(x)
        return (x - x.mean()) / (x.std() + 1e-9)
    combo = 0.6 * _norm(emb_scores) + 0.4 * _norm(bm25_scores)

    idxs = np.argsort(combo)[::-1][:top_k]
    out = []
    for i in idxs:
        snip = _highlight(texts[i], query)
        out.append({"file": files[i], "score": float(combo[i]), "snippet": snip})
    conn.close()
    return out
