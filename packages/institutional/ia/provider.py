"""Unified IA provider adapter.
- Uses OpenAI SDK if OPENAI_API_KEY is set
- Falls back to OpenRouter (OpenAI-compatible endpoint) if OPENROUTER_API_KEY is set
- Exposes: async generate_json(prompt: str, model: str, response_format: dict|None)
"""
import os, json, httpx, asyncio
from typing import Any, Dict, Optional

OPENAI_BASE = os.getenv("OPENAI_BASE", "https://api.openai.com/v1")
OPENROUTER_BASE = os.getenv("OPENROUTER_BASE", "https://openrouter.ai/api/v1")

def _headers():
    if os.getenv("OPENAI_API_KEY"):
        return {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}", "Content-Type": "application/json"}, OPENAI_BASE
    elif os.getenv("OPENROUTER_API_KEY"):
        return {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}", "Content-Type": "application/json"}, OPENROUTER_BASE
    else:
        return {"Content-Type": "application/json"}, OPENROUTER_BASE

async def generate_json(prompt: str, model: str, response_format: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers, base = _headers()
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    if response_format:
        payload["response_format"] = response_format
    url = f"{base}/chat/completions"
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "{}" )
        try:
            return json.loads(text)
        except Exception:
            # tenta extrair JSON na mão
            import re
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                return json.loads(m.group(0))
            return {"raw": text}
