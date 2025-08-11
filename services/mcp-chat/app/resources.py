import os, re

def list_resource_files(root: str):
    files = []
    for base, _dirs, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(('.txt','.md','.csv')):  # simples p/ DEV
                files.append(os.path.join(base,f))
    return files

def search_in_resources(root: str, query: str, limit: int = 5):
    hits = []
    files = list_resource_files(root)
    q = query.lower()
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
            if q in text.lower():
                # extrair pequeno trecho
                idx = text.lower().index(q)
                start = max(0, idx-200)
                end = min(len(text), idx+200)
                snippet = text[start:end].replace('\n',' ')
                hits.append({'file': path, 'snippet': snippet})
                if len(hits) >= limit:
                    break
        except Exception:
            continue
    return hits
