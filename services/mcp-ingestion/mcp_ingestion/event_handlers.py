"""
🔔 Event Handlers - MCP Ingestion Server
=======================================

Handlers de eventos específicos para o servidor de ingestão.
Implementa Event-Driven Architecture para comunicação assíncrona.

Responsabilidades:
- Reagir a eventos de upload de documentos
- Publicar eventos de análise concluída
- Monitorar saúde de outros serviços
"""

import logging
from typing import Dict, Any

from shared import (
    DomainEvent,
    EventHandler,
    EventType,
    publish_document_analyzed,
    log_operation
)

logger = logging.getLogger(__name__)

# =======================================================
# 📄 HANDLERS DE DOCUMENTOS
# =======================================================

class DocumentAnalysisCompleteHandler(EventHandler):
    """
    Handler que reage quando análise de documento é concluída
    
    Responsabilidades:
    - Notificar outros serviços sobre análise concluída
    - Preparar dados para persistência
    - Logs de auditoria
    """
    
    def __init__(self):
        self.name = "DocumentAnalysisCompleteHandler"
        logger.info(f"📋 {self.name} inicializado")
    
    async def handle(self, event: DomainEvent) -> None:
        """Processa evento de análise concluída"""
        try:
            logger.info(f"🔄 Processando análise concluída: {event.aggregate_id}")
            
            # Extrair dados do evento
            payload = event.payload
            analysis_type = payload.get("analysis_type")
            extracted_data = payload.get("extracted_data", {})
            processing_time = payload.get("processing_time", 0.0)
            
            # Log de auditoria
            log_operation(
                logger, 
                "document_analysis_completed",
                details={
                    "document_id": event.aggregate_id,
                    "analysis_type": analysis_type,
                    "processing_time": processing_time,
                    "data_fields": list(extracted_data.keys()) if extracted_data else [],
                    "correlation_id": event.correlation_id
                }
            )
            
            # Aqui poderia:
            # 1. Notificar Persistence Server que dados estão prontos
            # 2. Enviar email/notificação para usuário
            # 3. Aplicar regras de negócio adicionais
            # 4. Preparar dados para ML/Analytics
            
            logger.info(f"✅ Análise de {event.aggregate_id} processada com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar análise concluída: {e}")
            raise
    
    def can_handle(self, event_type: EventType) -> bool:
        """Verifica se pode processar este tipo de evento"""
        return event_type == EventType.DOCUMENT_ANALYZED
    
    @property
    def handler_name(self) -> str:
        return self.name

class DocumentUploadMonitorHandler(EventHandler):
    """
    Handler que monitora uploads de documentos
    
    Responsabilidades:
    - Estatísticas de upload
    - Validações adicionais
    - Preparação para análise
    """
    
    def __init__(self):
        self.name = "DocumentUploadMonitorHandler"
        self.upload_stats = {
            "total_uploads": 0,
            "total_size": 0,
            "uploads_by_type": {}
        }
        logger.info(f"📊 {self.name} inicializado")
    
    async def handle(self, event: DomainEvent) -> None:
        """Processa evento de upload de documento"""
        try:
            logger.info(f"📥 Monitorando upload: {event.aggregate_id}")
            
            # Extrair dados do evento
            payload = event.payload
            filename = payload.get("filename", "")
            file_size = payload.get("file_size", 0)
            user_id = payload.get("user_id")
            
            # Atualizar estatísticas
            self.upload_stats["total_uploads"] += 1
            self.upload_stats["total_size"] += file_size
            
            # Estatísticas por tipo de arquivo
            file_extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
            if file_extension not in self.upload_stats["uploads_by_type"]:
                self.upload_stats["uploads_by_type"][file_extension] = 0
            self.upload_stats["uploads_by_type"][file_extension] += 1
            
            # Log de auditoria
            log_operation(
                logger,
                "document_upload_monitored",
                details={
                    "document_id": event.aggregate_id,
                    "filename": filename,
                    "file_size": file_size,
                    "file_extension": file_extension,
                    "user_id": user_id,
                    "correlation_id": event.correlation_id,
                    "total_uploads_today": self.upload_stats["total_uploads"]
                }
            )
            
            # Validações adicionais poderiam ser aplicadas aqui:
            # - Verificar quota do usuário
            # - Detectar uploads suspeitos
            # - Preparar cache para análise
            
            logger.debug(f"📊 Stats atualizadas: {self.upload_stats}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao monitorar upload: {e}")
            raise
    
    def can_handle(self, event_type: EventType) -> bool:
        """Verifica se pode processar este tipo de evento"""
        return event_type == EventType.DOCUMENT_UPLOADED
    
    @property
    def handler_name(self) -> str:
        return self.name
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de upload"""
        return self.upload_stats.copy()

# =======================================================
# 🔧 HANDLERS DE SISTEMA
# =======================================================

class SystemHealthHandler(EventHandler):
    """
    Handler que monitora saúde do sistema
    
    Responsabilidades:
    - Reagir a falhas de health check
    - Monitorar performance
    - Alertas automáticos
    """
    
    def __init__(self):
        self.name = "SystemHealthHandler"
        self.health_incidents = []
        logger.info(f"🏥 {self.name} inicializado")
    
    async def handle(self, event: DomainEvent) -> None:
        """Processa eventos de saúde do sistema"""
        try:
            logger.warning(f"🚨 Incidente de saúde detectado: {event.aggregate_id}")
            
            # Registrar incidente
            incident = {
                "event_id": event.event_id,
                "timestamp": event.occurred_at,
                "aggregate_id": event.aggregate_id,
                "details": event.payload
            }
            self.health_incidents.append(incident)
            
            # Log crítico
            log_operation(
                logger,
                "health_incident_detected",
                details={
                    "incident_type": event.event_type.value,
                    "affected_component": event.aggregate_id,
                    "incident_details": event.payload,
                    "correlation_id": event.correlation_id
                }
            )
            
            # Aqui poderia:
            # 1. Enviar alertas para equipe
            # 2. Tentar restart automático
            # 3. Ativar modo degradado
            # 4. Notificar sistema de monitoramento
            
            logger.warning(f"🏥 Incidente registrado. Total de incidentes: {len(self.health_incidents)}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar incidente de saúde: {e}")
            raise
    
    def can_handle(self, event_type: EventType) -> bool:
        """Verifica se pode processar este tipo de evento"""
        return event_type in [
            EventType.HEALTH_CHECK_FAILED,
            EventType.ERROR_OCCURRED,
            EventType.MCP_SERVER_STOPPED
        ]
    
    @property
    def handler_name(self) -> str:
        return self.name
    
    def get_health_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de saúde"""
        return {
            "total_incidents": len(self.health_incidents),
            "recent_incidents": self.health_incidents[-5:] if self.health_incidents else []
        }

# =======================================================
# 🔧 FACTORY DE HANDLERS
# =======================================================

def create_ingestion_handlers() -> list[EventHandler]:
    """
    Factory que cria todos os handlers do Ingestion Server
    
    Returns:
        Lista de handlers configurados
    """
    handlers = [
        DocumentAnalysisCompleteHandler(),
        DocumentUploadMonitorHandler(),
        SystemHealthHandler()
    ]
    
    logger.info(f"🏭 Criados {len(handlers)} handlers para Ingestion Server")
    
    return handlers

def get_handler_statistics() -> Dict[str, Any]:
    """
    Retorna estatísticas agregadas de todos os handlers
    
    Returns:
        Dicionário com estatísticas
    """
    # Em uma implementação real, isso seria gerenciado por um registry
    return {
        "total_handlers": 3,
        "handler_types": [
            "DocumentAnalysisCompleteHandler",
            "DocumentUploadMonitorHandler", 
            "SystemHealthHandler"
        ]
    }