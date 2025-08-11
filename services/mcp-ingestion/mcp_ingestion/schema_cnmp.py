import os, csv, unicodedata, re
from typing import Dict, Any

def _slug_ascii(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = ''.join([c for c in s if not unicodedata.combining(c)])
    s = s.encode('ascii','ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+','_',s).strip('_')
    s = re.sub(r'_+','_',s)
    return s

def load_specs(csv_path: str) -> Dict[str, Dict[str, Any]]:
    specs = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Nome do Campo') or ''
            tipo = (row.get('Tipo') or '').strip()
            ml = row.get('maxLength')
            max_len = int(float(ml)) if ml else None
            key = _slug_ascii(name)
            specs[key] = {'original': name, 'type': tipo, 'maxLength': max_len}
    return specs
