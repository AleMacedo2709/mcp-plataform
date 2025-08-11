import os, json, textwrap
from typing import Dict, Any
from packages.institutional.ia.provider import generate_json
from .validator import load_specs, apply_specs
from .parser import extract_text

DEFAULT_MODEL = os.getenv('LLM_MODEL', 'openrouter/anthropic/claude-3.5-sonnet')
CSV_SCHEMA = os.getenv('CNMP_CSV_SCHEMA', '/app/mcp_ingestion/prompts/Formulario_CNMP_2025.csv')

PROMPT_TEMPLATE = """Você é um assistente do Ministério Público.
Extraia os 29 campos do formulário Prêmio CNMP a partir do texto abaixo.
Responda em JSON com chaves em snake_case correspondentes aos campos.

Texto:
---
{conteudo}
---
"""

async def analyze_file(file_path: str, model: str | None = None) -> Dict[str, Any]:
    text = extract_text(file_path) or ""
    if not text.strip():
        return {"error": "sem_texto_extraido"}
    prompt = PROMPT_TEMPLATE.format(conteudo=text[:30000])
    model = model or DEFAULT_MODEL
    j = await generate_json(prompt, model=model, response_format=None)
    # j pode ser dict ou {raw: "..."} ou string
    if isinstance(j, dict) and 'raw' in j and isinstance(j['raw'], str):
        try:
            j = json.loads(j['raw'])
        except Exception:
            j = {"raw": j['raw']}
    specs = load_specs(CSV_SCHEMA)
    if isinstance(j, dict):
        j = apply_specs(j, specs)
    return j
