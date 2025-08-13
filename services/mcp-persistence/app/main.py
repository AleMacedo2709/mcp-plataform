from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
import sys
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
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from .core.settings import settings
from .api.routers import projects, reports

app = FastAPI(title="MCP Persistence API", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # PROD: sem fallback "*"
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"],
    allow_headers=["Authorization","Content-Type","X-Requested-With","x-role","x-user","x-origin"],
)

# Rate limiting básico
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
from slowapi.middleware import SlowAPIMiddleware
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def _rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENVIRONMENT}

@app.get("/readiness")
def readiness():
    # Verifica conexão com DB
    try:
        from .db.session import SessionLocal
        from sqlalchemy import text
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=f"not ready: {e}")


import os
INCLUDE_INST = os.getenv("INCLUDE_INSTITUTIONAL_ROUTES", "false").lower() == "true"
if INCLUDE_INST:
    try:
        from .institutional_routes import api as inst_api, root as inst_root, tasks as inst_tasks, upload as inst_upload
        app.include_router(inst_root.router, tags=["inst-root"])
        app.include_router(inst_api.router, prefix="/inst/api", tags=["inst-api"])
        app.include_router(inst_tasks.router, prefix="/inst/tasks", tags=["inst-tasks"])
        app.include_router(inst_upload.router, prefix="/inst/upload", tags=["inst-upload"])
    except Exception:
        # Rotas legadas removidas
        pass


from fastapi import Request
USE_AUTH = os.getenv("USE_AUTH", "false").lower() == "true"
if USE_AUTH:
    from .security.entra import add_auth_middleware
    add_auth_middleware(app)
else:
    # Em produção, autenticação deve estar ativa
    if (settings.ENVIRONMENT or "local") == "production":
        raise RuntimeError("USE_AUTH must be true in production")


# Auto-migration on startup (DEV only)
@app.on_event("startup")
def _auto_migrate_dev():
    # Executa auto-migration apenas em local/dev e somente se explicitamente habilitado
    import os
    if (settings.ENVIRONMENT or "local") in ("local","dev") and os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        try:
            from alembic.config import Config
            from alembic import command
            cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
            command.upgrade(cfg, "head")
        except Exception as e:
            print(f"[WARN] Auto-migration failed: {e}")


# Safety net: align schema for recent columns/tables in dev/local
@app.on_event("startup")
def _ensure_schema_columns():
    try:
        from sqlalchemy import text
        from .db.session import SessionLocal
        with SessionLocal() as db:
            # add missing columns if they don't exist
            db.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS unidade_gestora VARCHAR(200)"))
            db.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS selo VARCHAR(50)"))
            # drop legacy columns if they exist
            db.execute(text("ALTER TABLE projects DROP COLUMN IF EXISTS contatos"))
            db.execute(text("ALTER TABLE projects DROP COLUMN IF EXISTS comprovacao_dos_resultados"))
            db.execute(text("ALTER TABLE projects DROP COLUMN IF EXISTS categoria"))
            db.commit()
    except Exception as _e:
        # do not crash app in case of permissions; logs already show SQL errors if any
        print(f"[WARN] ensure_schema_columns: {_e}")

app.add_middleware(RequestIdMiddleware)

configure_json_logging('mcp-persistence')
app.add_middleware(MetricsMiddleware, service='mcp-persistence')
from fastapi import APIRouter, Depends
from .security.deps import require_roles
metrics_router = APIRouter()
_protect_metrics = (settings.ENVIRONMENT or "local") == "production" or os.getenv("PROTECT_METRICS", "true").lower() == "true"
_deps = [Depends(require_roles('admin'))] if _protect_metrics else None
metrics_router.add_api_route('/metrics', metrics_endpoint(), methods=['GET'], dependencies=_deps)
app.include_router(metrics_router)

setup_tracing('mcp-persistence')

app.add_middleware(SecurityHeadersMiddleware)

# Load shared env
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass

# Static serving for uploaded files
try:
    import os as _os
    _upload_dir = _os.getenv("UPLOAD_DIR", "/data/uploads")
    _os.makedirs(_upload_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=_upload_dir), name="uploads")
except Exception:
    # In dev, failing to mount static shouldn't crash the app
    pass
