"""
🔍 MCP Server de Ingestão e Análise
=================================

Responsabilidades:
- Receber documentos (PDF, DOCX)
- Extrair texto com Marker-PDF
- Analisar com LLM usando contratos JSON
- Retornar dados estruturados

Conforme PRD - Seção 5.2
"""

import os
import time
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import logging
from packages.institutional.tools.jsonlog import configure_json_logging
from packages.institutional.tools.tracing import setup_tracing
from packages.institutional.tools.security_headers import SecurityHeadersMiddleware
from packages.institutional.tools.metrics import MetricsMiddleware, metrics_endpoint
from packages.institutional.tools.telemetry import RequestIdMiddleware, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 🔧 Sistema padronizado de exceções e logging
from shared import (
    get_ingestion_logger,
    MCPBaseException,
    ErrorCode,
    FileProcessingError,
    LLMError,
    create_error_response,
    get_http_status_code,
    log_operation,
    log_performance,
    # Sistema de eventos
    event_publisher,
    subscribe_handler,
    EventType,
    create_correlation_id,
    publish_document_uploaded,
    publish_document_analyzed,
    # Sistema de debug
    async_debug_decorator,
    setup_debug_middleware,
    quick_debug_setup
)

from services.document_parser import DocumentParser
from services.llm_analyzer import LLMAnalyzer
from services.event_handlers import create_ingestion_handlers

# Configuração padronizada de logging (com debug se habilitado)
logger = quick_debug_setup("ingestion")

# Configuração do FastAPI
app = FastAPI(
    title="MCP Server - Ingestão e Análise",
    description="Servidor especializado em análise de documentos com IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de debug (se habilitado)
if os.getenv("ENABLE_DEBUG", "false").lower() == "true":
    setup_debug_middleware(app)
    logger.info("🐛 Debug middleware ativado")

# ========== TRATAMENTO GLOBAL DE EXCEÇÕES ==========

@app.exception_handler(MCPBaseException)
async def mcp_exception_handler(request: Request, exc: MCPBaseException):
    """Handler para exceções MCP padronizadas"""
    status_code = get_http_status_code(exc.error_code)
    
    logger.error(
        f"🚨 Exceção MCP tratada: {exc.message}",
        extra={
            "trace_id": exc.trace_id,
            "error_code": exc.error_code.value,
            "user_message": exc.user_message,
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status_code,
        content=create_error_response(exc, status_code)
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler para exceções não tratadas"""
    mcp_error = MCPBaseException(
        message=f"Erro não tratado: {str(exc)}",
        error_code=ErrorCode.INTERNAL_ERROR,
        user_message="Erro interno do servidor. Tente novamente.",
        original_exception=exc,
        context={
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=500,
        content=create_error_response(mcp_error, 500)
    )

# Inicializar serviços
document_parser = DocumentParser()
llm_analyzer = LLMAnalyzer(prompts_dir="prompts")

# ========== CONFIGURAÇÃO DE EVENTOS ==========

# Registrar handlers de eventos
event_handlers = create_ingestion_handlers()
for handler in event_handlers:
    # Registrar handler para todos os tipos de evento que ele pode processar
    for event_type in EventType:
        if handler.can_handle(event_type):
            subscribe_handler(event_type, handler)

logger.info(f"🔔 Registrados {len(event_handlers)} event handlers")

@app.get("/health")
async def health_check():
    """Health check do MCP Server de Ingestão"""
    try:
        # Verificar serviços críticos
        health_status = {
            "status": "healthy",
            "server": "MCP Ingestion Server",
            "version": "1.0.0",
            "timestamp": time.time(),
            "services": {
                "document_parser": "healthy",
                "llm_analyzer": "healthy"
            }
        }
        
        log_operation(logger, "health_check", details=health_status)
        return health_status
        
    except Exception as e:
        error = MCPBaseException(
            message=f"Health check failed: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            user_message="Serviço temporariamente indisponível",
            original_exception=e
        )
        
        return JSONResponse(
            status_code=503,
            content=create_error_response(error, 503)
        )

@app.get("/capabilities")
async def get_capabilities():
    """Retorna as capacidades do servidor (conforme protocolo MCP)"""
    return {
        "tools": [
            {
                "name": "analyze_document",
                "description": "Analisa documentos e extrai dados estruturados",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "format": "binary"},
                        "analysis_type": {"type": "string", "enum": ["cnmp_project"]}
                    },
                    "required": ["file", "analysis_type"]
                }
            }
        ],
        "prompts": llm_analyzer.list_available_prompts(),
        "resources": [
            {
                "name": "marker_pdf",
                "description": "Biblioteca para extração de texto de PDFs",
                "type": "document_parser"
            }
        ]
    }

@app.post("/analyze")
@async_debug_decorator
async def analyze_document(
    file: UploadFile = File(...),
    analysis_type: str = "analyze_project_document_cnmp"
):
    """
    🎯 Endpoint principal de análise de documentos
    
    Fluxo conforme PRD:
    1. Recebe arquivo
    2. Extrai texto com Marker-PDF (Recursos)
    3. Carrega contrato de prompt JSON
    4. Combina texto + prompt para LLM
    5. Retorna dados estruturados
    6. 🔔 Publica eventos de domínio
    """
    start_time = time.time()
    correlation_id = create_correlation_id()
    document_id = f"doc_{int(time.time())}_{file.filename.replace('.', '_')}"
    
    try:
        logger.info(f"📄 Iniciando análise: {file.filename} ({analysis_type}) - ID: {document_id}")
        
        # Validação do arquivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nome do arquivo é obrigatório")
        
        # Validar tipo de arquivo
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Use: {', '.join(allowed_extensions)}"
            )
        
        # Validar tamanho (100MB)
        file_content = await file.read()
        if len(file_content) > 100 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Arquivo muito grande (máx: 100MB)")
        
        # 🔔 EVENTO: Documento enviado
        await publish_document_uploaded(
            document_id=document_id,
            filename=file.filename,
            file_size=len(file_content),
            correlation_id=correlation_id
        )
        
        # 1. EXTRAÇÃO DE TEXTO (Recursos - Marker-PDF)
        logger.info("🔍 Extraindo texto do documento...")
        extracted_text = document_parser.parse_document(file_content, file.filename)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise HTTPException(
                status_code=400, 
                detail="Não foi possível extrair texto suficiente do documento"
            )
        
        # 2. ANÁLISE COM LLM (Prompt + LLM)
        logger.info(f"🤖 Analisando com IA usando contrato: {analysis_type}")
        structured_data = llm_analyzer.analyze_with_llm(analysis_type, extracted_text)
        
        processing_time = time.time() - start_time
        
        logger.info(f"✅ Análise concluída em {processing_time:.2f}s")
        
        # 🔔 EVENTO: Análise concluída
        await publish_document_analyzed(
            document_id=document_id,
            analysis_type=analysis_type,
            extracted_data=structured_data,
            processing_time=processing_time,
            correlation_id=correlation_id
        )
        
        return {
            "status": "success",
            "data": structured_data,
            "metadata": {
                "document_id": document_id,
                "filename": file.filename,
                "file_size": len(file_content),
                "text_length": len(extracted_text),
                "processing_time": processing_time,
                "analysis_type": analysis_type,
                "server": "mcp_ingestion_server",
                "timestamp": time.time(),
                "correlation_id": correlation_id
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor de ingestão: {str(e)}"
        )

@app.get("/prompts")
async def list_prompts():
    """Lista contratos de prompt disponíveis"""
    return {
        "available_prompts": llm_analyzer.list_available_prompts(),
        "server": "mcp_ingestion_server"
    }

@app.get("/prompts/{prompt_name}")
async def get_prompt_details(prompt_name: str):
    """Detalhes de um contrato de prompt específico"""
    try:
        prompt_details = llm_analyzer.get_prompt_contract(prompt_name)
        return {
            "prompt": prompt_details,
            "server": "mcp_ingestion_server"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

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

configure_json_logging('mcp-ingestion')
app.add_middleware(MetricsMiddleware, service='mcp-ingestion')
from fastapi import APIRouter
metrics_router = APIRouter()
metrics_router.add_api_route('/metrics', metrics_endpoint(), methods=['GET'])
app.include_router(metrics_router)

setup_tracing('mcp-ingestion')

app.add_middleware(SecurityHeadersMiddleware)


@app.get("/tasks/{task_id}")
def task_status(task_id: str):
    c = get_celery()
    res = c.AsyncResult(task_id)
    return {"id": task_id, "status": res.status, "result": res.result if res.successful() else None}

# Load shared env only
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass
