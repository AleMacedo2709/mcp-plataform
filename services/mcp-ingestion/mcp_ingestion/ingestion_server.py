"""MCP Ingestion API: upload e análise de documentos (DEV minimal)."""

import os
import sys
import time
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Garantir PYTHONPATH
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

from .document_parser import DocumentParser
from .llm_analyzer import LLMAnalyzer

app = FastAPI(title="MCP Ingestion API", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["Authorization","Content-Type","X-Requested-With"]
)

app.add_middleware(RequestIdMiddleware)
configure_json_logging('mcp-ingestion')
app.add_middleware(MetricsMiddleware, service='mcp-ingestion')
setup_tracing('mcp-ingestion')
# CSP mais estrita em produção (permitir connect à API/INGESTION/CHAT via CORS)
_env = os.getenv("ENVIRONMENT", "local").lower()
_csp = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'" + (" *" if _env != 'production' else "") + "; frame-ancestors 'none'"
app.add_middleware(SecurityHeadersMiddleware, csp=_csp)

document_parser = DocumentParser()
# Garantir caminho absoluto para os contratos de prompt
_prompts_dir = str((Path(__file__).resolve().parent / "prompts").resolve())
llm_analyzer = LLMAnalyzer(prompts_dir=_prompts_dir)


@app.get("/health")
def health():
    return {"status": "ok", "env": os.getenv("ENVIRONMENT", "local")}


# Rate limiting (opcional; inicia somente se slowapi disponível)
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    from fastapi.responses import JSONResponse
    from slowapi.middleware import SlowAPIMiddleware
    limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])  # geral
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    def _rate_limit_handler(request, exc):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
except Exception:
    limiter = None

@app.post("/analyze")
@(limiter.limit("10/minute") if limiter else (lambda f: f))
async def analyze_document(request: Request, file: UploadFile = File(...), analysis_type: str = "analyze_project_document_cnmp"):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nome do arquivo é obrigatório")

    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")

    content = await file.read()
    if len(content) > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máx: 100MB)")

    try:
        text = document_parser.parse_document(content, file.filename)
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto suficiente do documento")
        data = llm_analyzer.analyze_with_llm(analysis_type, text)
        return {
            "status": "success",
            "data": data,
            "analysis": data,
            "metadata": {
                "filename": file.filename,
                "file_size": len(content),
                "text_length": len(text),
                "analysis_type": analysis_type,
                "timestamp": time.time(),
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})


# Metrics endpoint (proteção simples em PROD)
from fastapi import APIRouter
import os as _os
_protect = (_os.getenv("ENVIRONMENT", "local").lower() == "production") or (_os.getenv("PROTECT_METRICS", "true").lower() == "true")

def _require_admin(req: Request = None):
    if not _protect:
        return True
    try:
        roles = (req.headers.get('x-role','') if req else '').lower()
        if 'admin' in roles:
            return True
    except Exception:
        pass
    from fastapi import HTTPException
    raise HTTPException(status_code=403, detail='forbidden')

metrics_router = APIRouter()
metrics_router.add_api_route('/metrics', metrics_endpoint(), methods=['GET'], dependencies=[Depends(_require_admin)] if _protect else None)
app.include_router(metrics_router)


@app.get("/prompts")
def list_prompts():
    return {
        "available_prompts": llm_analyzer.list_available_prompts(),
    }


@app.get("/prompts/{prompt_name}")
def get_prompt(prompt_name: str):
    try:
        return llm_analyzer.get_prompt_contract(prompt_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


