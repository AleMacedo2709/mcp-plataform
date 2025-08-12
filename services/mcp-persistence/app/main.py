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
from .core.settings import settings
from .api.routers import projects, reports

app = FastAPI(title="MCP Persistence API", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENVIRONMENT}


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


# Auto-migration on startup (DEV only)
@app.on_event("startup")
def _auto_migrate_dev():
    if (settings.ENVIRONMENT or "local") in ("local","dev"):
        try:
            from alembic.config import Config
            from alembic import command
            import os
            cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
            command.upgrade(cfg, "head")
        except Exception as e:
            # Em dev, apenas logar
            print(f"[WARN] Auto-migration failed: {e}")

app.add_middleware(RequestIdMiddleware)

configure_json_logging('mcp-persistence')
app.add_middleware(MetricsMiddleware, service='mcp-persistence')
from fastapi import APIRouter
metrics_router = APIRouter()
metrics_router.add_api_route('/metrics', metrics_endpoint(), methods=['GET'])
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
