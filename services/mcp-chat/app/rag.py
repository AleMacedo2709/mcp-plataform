import os, re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _chunks(text, size=800, overlap=100):
    for i in range(0, max(len(text)-1, 0), max(size-overlap,1)):
        yield text[i:i+size]

def _highlight(snippet: str, query: str):
    terms = [re.escape(t) for t in query.lower().split() if len(t) > 2]
    if not terms:
        return snippet[:400]
    pat = re.compile(r'(' + '|'.join(terms) + r')', re.I)
    return pat.sub(lambda m: f"**{m.group(0)}**", snippet)[:600]

class SimpleVectorIndex:
    def __init__(self, docs: List[Dict[str,str]]):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(max_features=20000)
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in docs])

    def search(self, query: str, top_k: int = 5):
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix)[0]
        idxs = sims.argsort()[::-1][:top_k]
        results = []
        for i in idxs:
            d = self.docs[i]
            snip = _highlight(d["text"][:800], query)
            results.append({"file": d["file"], "score": float(sims[i]), "snippet": snip})
        return results

def build_index(resource_root: str) -> SimpleVectorIndex | None:
    texts = []
    for base, _dirs, files in os.walk(resource_root):
        for f in files:
            if f.lower().endswith((".txt",".md",".csv")):
                path = os.path.join(base,f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        txt = fh.read()
                        for ch in _chunks(txt):
                            if ch.strip():
                                texts.append({"file": path, "text": ch})
                except Exception:
                    continue
    if not texts:
        return None
    return SimpleVectorIndex(texts)


# Embeddings (opcional): tenta usar sentence-transformers; fallback TF-IDF
try:
    from sentence_transformers import SentenceTransformer
    _EMB_MODEL = SentenceTransformer(os.getenv("EMB_MODEL","all-MiniLM-L6-v2"))
except Exception as _e:
    _EMB_MODEL = None

def build_embed_index(resource_root: str):
    if not _EMB_MODEL:
        return None
    docs = []
    for base, _dirs, files in os.walk(resource_root):
        for f in files:
            if f.lower().endswith(('.txt','.md','.csv')):
                path = os.path.join(base,f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        txt = fh.read()
                        for ch in _chunks(txt):
                            if ch.strip():
                                docs.append({'file': path, 'text': ch})
                except Exception:
                    continue
    if not docs:
        return None
    embs = _EMB_MODEL.encode([d['text'] for d in docs], show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
    return {'docs': docs, 'embs': embs}

def search_embed(index, query: str, top_k: int = 5):
    if not index or not _EMB_MODEL:
        return []
    qv = _EMB_MODEL.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
    import numpy as np
    sims = (index['embs'] @ qv).astype(float)
    idxs = sims.argsort()[::-1][:top_k]
    out = []
    for i in idxs:
        d = index['docs'][i]
        out.append({'file': d['file'], 'score': float(sims[i]), 'snippet': _highlight(d['text'][:800], query)})
    return out
