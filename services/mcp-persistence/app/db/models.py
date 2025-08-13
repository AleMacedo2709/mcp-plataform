from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .session import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(320), nullable=False, index=True)
    nome_da_iniciativa = Column(String(300), nullable=False)
    tipo_de_iniciativa = Column(String, nullable=True, index=True)
    classificacao = Column(String, nullable=True, index=True)
    unidade_gestora = Column(String(200), nullable=True)
    selo = Column(String(50), nullable=True)  # valores esperados: PGJ, CG Cidadã
    natureza_da_iniciativa = Column(String(100), nullable=True)
    iniciativa_vinculada = Column(String(300), nullable=True)
    objetivo_estrategico_pen_mp = Column(String, nullable=True)
    programa_pen_mp = Column(String, nullable=True)
    promocao_do_objetivo_estrategico = Column(String(100), nullable=True)
    data_inicial_de_operacao = Column(String(300), nullable=True)
    fase_de_implementacao = Column(String, nullable=True, index=True)
    descricao = Column(String(1000), nullable=False)
    estimativa_de_recursos = Column(String(200), nullable=True)
    publico_impactado = Column(String(100), nullable=True)
    orgaos_envolvidos = Column(String(300), nullable=True)
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
    # comprovacao_dos_resultados removido; agora tabela relacionada
    capa_da_iniciativa = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    cover = relationship("ProjectCover", back_populates="project", uselist=False, cascade="all, delete-orphan")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    actions = relationship("ProjectAction", back_populates="project", cascade="all, delete-orphan")
    contacts = relationship("ProjectContact", back_populates="project", cascade="all, delete-orphan")
    results = relationship("ProjectResultProof", back_populates="project", cascade="all, delete-orphan")
    awards = relationship("ProjectCnmpAward", back_populates="project", cascade="all, delete-orphan")


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


class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    original_name = Column(String(500), nullable=False)
    stored_path = Column(String(1000), nullable=False)
    content_type = Column(String(200), nullable=True)
    size_bytes = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class ProjectCover(Base):
    __tablename__ = 'project_covers'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    original_name = Column(String(500), nullable=False)
    stored_path = Column(String(1000), nullable=False)
    content_type = Column(String(200), nullable=True)
    size_bytes = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="cover")

class ProjectMember(Base):
    __tablename__ = 'project_members'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(320), nullable=False)
    role = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="members")


class ProjectAction(Base):
    __tablename__ = 'project_actions'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    descricao = Column(String(1000), nullable=False)  # Ação (descritivo)
    area_responsavel = Column(String(300), nullable=True)
    email_responsavel = Column(String(320), nullable=True)
    progresso = Column(String(50), nullable=True)  # Não iniciada, Em andamento, Concluída, Suspensa
    inicio_previsto = Column(String(50), nullable=True)
    termino_previsto = Column(String(50), nullable=True)
    inicio_efetivo = Column(String(50), nullable=True)
    termino_efetivo = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="actions")


class ProjectLike(Base):
    __tablename__ = 'project_likes'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    user_email = Column(String(320), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ProjectContact(Base):
    __tablename__ = 'project_contacts'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(320), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="contacts")


class ProjectResultProof(Base):
    __tablename__ = 'project_result_proofs'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    data_da_coleta = Column(String(50), nullable=True)
    resultado = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="results")


class ProjectCnmpAward(Base):
    __tablename__ = 'project_cnmp_awards'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    ano = Column(String(10), nullable=False)
    categoria = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="awards")