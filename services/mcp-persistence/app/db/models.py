from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .session import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(320), nullable=False)
    nome_da_iniciativa = Column(String(300), nullable=False)
    tipo_de_iniciativa = Column(String, nullable=True)
    classificacao = Column(String, nullable=True)
    natureza_da_iniciativa = Column(String(100), nullable=True)
    iniciativa_vinculada = Column(String(300), nullable=True)
    objetivo_estrategico_pen_mp = Column(String, nullable=True)
    programa_pen_mp = Column(String, nullable=True)
    promocao_do_objetivo_estrategico = Column(String(100), nullable=True)
    data_inicial_de_operacao = Column(String(300), nullable=True)
    fase_de_implementacao = Column(String, nullable=True)
    descricao = Column(String(1000), nullable=False)
    estimativa_de_recursos = Column(String(200), nullable=True)
    publico_impactado = Column(String(100), nullable=True)
    orgaos_envolvidos = Column(String(300), nullable=True)
    contatos = Column(String(300), nullable=True)
    desafio_1 = Column(String(100), nullable=True)
    desafio_2 = Column(String(100), nullable=True)
    desafio_3 = Column(String(100), nullable=True)
    resolutividade = Column(String(500), nullable=True)
    inovacao = Column(String(500), nullable=True)
    transparencia = Column(String(500), nullable=True)
    proatividade = Column(String(500), nullable=True)
    cooperacao = Column(String(500), nullable=True)
    resultado_1 = Column(String(100), nullable=True)
    resultado_2 = Column(String(100), nullable=True)
    resultado_3 = Column(String(100), nullable=True)
    comprovacao_dos_resultados = Column(String, nullable=True)
    capa_da_iniciativa = Column(String, nullable=True)
    categoria = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String(64), primary_key=True, index=True)  # Celery task_id
    type = Column(String(100), nullable=False)  # e.g., 'ingest_analyze'
    filename = Column(String(500), nullable=True)
    owner = Column(String(320), nullable=False)
    status = Column(String(50), nullable=False, default='queued')
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
