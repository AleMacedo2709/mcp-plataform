import csv, os, unicodedata, re
from typing import Dict, Any

def _slug_ascii(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.encode('ascii','ignore').decode('ascii').lower()
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_')
    s = re.sub(r'_+', '_', s)
    return s

def load_specs(csv_path: str) -> Dict[str, Dict[str, Any]]:
    specs = {}
    if not os.path.exists(csv_path):
        return specs
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get('Nome do Campo') or '').strip()
            if not name: continue
            ml = row.get('maxLength'); max_len = int(float(ml)) if ml else None
            specs[_slug_ascii(name)] = {'original': name, 'maxLength': max_len}
    return specs

def apply_specs(data: dict, specs: Dict[str, Dict[str, Any]]) -> dict:
    if not specs: return data
    out = dict(data)
    for k, v in list(out.items()):
        if k in specs and isinstance(v, str):
            ml = specs[k].get('maxLength')
            if ml: out[k] = v[:ml]
    return out
