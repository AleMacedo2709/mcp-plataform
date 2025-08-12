from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
import sys
import logging
try:
    _app_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(_app_root))
    sys.path.insert(0, str(_app_root / 'packages'))
except Exception:
    pass

from packages.institutional.tools.jsonlog import configure_json_logging
from packages.institutional.tools.tracing import setup_tracing
from packages.institutional.tools.security_headers import SecurityHeadersMiddleware
from packages.institutional.tools.metrics import MetricsMiddleware, metrics_endpoint
from packages.institutional.tools.telemetry import RequestIdMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from .core.settings import settings
from .db import search_projects, get_project
from .resources import search_in_resources
from .rag import build_index, build_embed_index, search_embed
from .rag_persistent import build_persistent_index, search_hybrid
from packages.institutional.ia.provider import generate_json

from .mcp_server import mcp  # MCP SDK server

app = FastAPI(title="MCP Chat (DEV)", version="0.2.0")

class AskPayload(BaseModel):
    question: str
    project_id: Optional[int] = None

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENVIRONMENT}

@app.post("/ask")
def ask(payload: AskPayload):
    q = (payload.question or "").strip()
    if not q:
        log.warning('pergunta vazia'); return {"answer": "Pergunta vazia."}

    # Heurística simples: se mencionar 'projeto' + número, detalha; se 'resource', busca; senão, busca projetos.
    import re
    m = re.search(r"(projeto\s*#?)(\d+)", q, re.I)
    if m:
        pid = int(m.group(2))
        p = get_project(pid)
        if p:
            return {"answer": f"Projeto {pid}: {p.get('nome_da_iniciativa')} | Fase: {p.get('fase_de_implementacao')}", "data": p}
        log.info('projeto não encontrado: %s', pid); return {"answer": f"Projeto {pid} não encontrado."}

    if "resource" in q.lower() or "documento" in q.lower() or "buscar" in q.lower():
        hits = []
        hits = search_hybrid(q, top_k=5)
        if not hits:
            if '_EMB_INDEX' in globals() and _EMB_INDEX:
                hits = search_embed(_EMB_INDEX, q, top_k=5)
        if not hits:
            hits = search_in_resources(settings.RESOURCE_DIR, q, limit=3)
        if not hits and '_RAG_INDEX' in globals() and _RAG_INDEX:
            hits = _RAG_INDEX.search(q, top_k=5)
        if hits:
            return {"answer": f"Encontrei {len(hits)} referência(s).", "hits": hits}
        return {"answer": "Nenhuma referência em resources."}

    results = search_projects(q, limit=5)
    if results:
        nomes = "; ".join([f"#{r['id']} {r['nome_da_iniciativa']}" for r in results])
        return {"answer": f"Encontrei projetos: {nomes}", "results": results}

    return {"answer": "Não encontrei projetos correspondentes. Tente outro termo."}

# Nota: execução MCP stdio será por entrypoint separado, mas o servidor HTTP está pronto.

from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def ws_chat(ws: WebSocket):
    await ws.accept()
    try:
        await ws.send_json({"type":"welcome","message":"MCP Chat WebSocket pronto."})
        while True:
            data = await ws.receive_json()
            question = data.get("question") or ""
            resp = ask(AskPayload(question=question))  # reuso da lógica HTTP
            await ws.send_json({"type":"answer","payload":resp})
    except WebSocketDisconnect:
        return


@app.on_event("startup")
def _build_rag_index():
    global _RAG_INDEX, _EMB_INDEX
    try:
        _RAG_INDEX = build_index(settings.RESOURCE_DIR)
        _EMB_INDEX = build_embed_index(settings.RESOURCE_DIR)
        if _RAG_INDEX:
            print(f"[RAG] Index carregado com {len(_RAG_INDEX.docs)} docs")
        else:
            print("[RAG] Nenhum documento de resource encontrado")
    except Exception as e:
        print(f"[RAG] Falha ao indexar resources: {e}")


# Auth toggle (placeholder) - quando USE_AUTH=true, aplicar middleware institucional
import os as _os
_USE_AUTH = _os.getenv("USE_AUTH", "false").lower() == "true"
if _USE_AUTH:
    try:
        from packages.institutional.auth.auth.entra import add_auth_middleware as _add_auth
        _add_auth(app)  # type: ignore
    except Exception as e:
        print(f"[WARN] Auth não habilitada: {e}")

app.add_middleware(RequestIdMiddleware)


async def _summarize_answer(question: str, payload: dict) -> dict:
    """Use unified IA provider to reformulate/explicar respostas."""
    try:
        model = os.getenv("LLM_MODEL", "openrouter/anthropic/claude-3.5-sonnet")
        prompt = f"""Você é um assistente do Ministério Público.
Pergunta do usuário: {question}

Abaixo estão dados retornados pelo sistema (JSON):
{payload}

Responda em português, de forma objetiva e clara, com 3 partes:
1) Síntese direta
2) Próximos passos sugeridos (bullets)
3) Se houver, cite projetos relevantes por id e nome
"""
        j = await generate_json(prompt, model=model, response_format=None)
        # Quando provider retorna {raw: "..."} ou string, padronizamos
        if isinstance(j, dict) and "raw" in j and isinstance(j["raw"], str):
            return {"explanation": j["raw"]}
        if isinstance(j, str):
            return {"explanation": j}
        # Se vier JSON, devolvemos como explanation ou full
        return {"explanation": j if isinstance(j, dict) else str(j)}
    except Exception as e:
        return {"explanation": f"[sem IA para explicação] {e}"}

configure_json_logging('mcp-chat')
app.add_middleware(MetricsMiddleware, service='mcp-chat')
from fastapi import APIRouter
metrics_router = APIRouter()
metrics_router.add_api_route('/metrics', metrics_endpoint(), methods=['GET'])
app.include_router(metrics_router)


@app.on_event("startup")
def _build_persistent_index():
    try:
        s = build_persistent_index(settings.RESOURCE_DIR)
        print(f"[RAG] Persistent index built: {s}")
    except Exception as e:
        print(f"[RAG] Persistent index failed: {e}")

setup_tracing('mcp-chat')

app.add_middleware(SecurityHeadersMiddleware)

log = logging.getLogger('mcp_chat')


@app.post("/reindex")
def reindex():
    # Rebuild persistent index on demand
    try:
        s = build_persistent_index(settings.RESOURCE_DIR)
        return {"status":"ok","stats":s}
    except Exception as e:
        return {"status":"error","detail":str(e)}

# Load shared env only
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass
