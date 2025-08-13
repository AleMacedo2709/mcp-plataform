from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    owner: str | None = Field(None, max_length=320)  # preenchido no backend
    nome_da_iniciativa: str = Field(..., max_length=300)
    tipo_de_iniciativa: str | None = Field(None, max_length=300)
    classificacao: str | None = Field(None, max_length=300)
    unidade_gestora: Optional[str] = Field(None, max_length=200)
    selo: Optional[str] = Field(None, max_length=50)
    natureza_da_iniciativa: str | None = Field(None, max_length=100)
    iniciativa_vinculada: str | None = Field(None, max_length=300)
    objetivo_estrategico_pen_mp: str | None = Field(None, max_length=300)
    programa_pen_mp: str | None = Field(None, max_length=300)
    promocao_do_objetivo_estrategico: str | None = Field(None, max_length=100)
    data_inicial_de_operacao: str | None = Field(None, max_length=300)
    fase_de_implementacao: str | None = Field(None, max_length=300)
    descricao: str = Field(..., max_length=1000)
    estimativa_de_recursos: str | None = Field(None, max_length=200)
    publico_impactado: str | None = Field(None, max_length=100)
    orgaos_envolvidos: str | None = Field(None, max_length=300)
    desafio_1: str | None = Field(None, max_length=100)
    desafio_2: str | None = Field(None, max_length=100)
    desafio_3: str | None = Field(None, max_length=100)
    resolutividade: str | None = Field(None, max_length=500)
    inovacao: str | None = Field(None, max_length=500)
    transparencia: str | None = Field(None, max_length=500)
    proatividade: str | None = Field(None, max_length=500)
    cooperacao: str | None = Field(None, max_length=500)
    resultado_1: str | None = Field(None, max_length=100)
    resultado_2: str | None = Field(None, max_length=100)
    resultado_3: str | None = Field(None, max_length=100)
    # comprovacao_dos_resultados removido; usar entidade relacionada
    capa_da_iniciativa: str | None = Field(None, max_length=300)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    id: str
    type: str
    filename: str | None = None
    owner: str
    status: str
    result: str | None = None

class TaskOut(TaskBase):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True


# --- Project Members (Equipe) ---
class ProjectMemberBase(BaseModel):
    name: str = Field(..., max_length=200)
    email: str = Field(..., max_length=320)
    role: Optional[str] = Field(None, max_length=100)

class ProjectMemberCreate(ProjectMemberBase):
    pass

class ProjectMemberUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=320)
    role: Optional[str] = Field(None, max_length=100)

class ProjectMemberOut(ProjectMemberBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True


# --- Project Actions ---
class ProjectActionBase(BaseModel):
    descricao: str = Field(..., max_length=1000)
    area_responsavel: Optional[str] = Field(None, max_length=300)
    email_responsavel: Optional[str] = Field(None, max_length=320)
    progresso: Optional[str] = Field(None, max_length=50)
    inicio_previsto: Optional[str] = Field(None, max_length=50)
    termino_previsto: Optional[str] = Field(None, max_length=50)
    inicio_efetivo: Optional[str] = Field(None, max_length=50)
    termino_efetivo: Optional[str] = Field(None, max_length=50)

class ProjectActionCreate(ProjectActionBase):
    pass

class ProjectActionUpdate(BaseModel):
    descricao: Optional[str] = Field(None, max_length=1000)
    area_responsavel: Optional[str] = Field(None, max_length=300)
    email_responsavel: Optional[str] = Field(None, max_length=320)
    progresso: Optional[str] = Field(None, max_length=50)
    inicio_previsto: Optional[str] = Field(None, max_length=50)
    termino_previsto: Optional[str] = Field(None, max_length=50)
    inicio_efetivo: Optional[str] = Field(None, max_length=50)
    termino_efetivo: Optional[str] = Field(None, max_length=50)

class ProjectActionOut(ProjectActionBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True


# --- Likes ---
class ProjectLikeOut(BaseModel):
    project_id: int
    likes: int


# --- Contacts ---
class ProjectContactBase(BaseModel):
    nome: str = Field(..., max_length=200)
    email: str = Field(..., max_length=320)

class ProjectContactCreate(ProjectContactBase):
    pass

class ProjectContactUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=320)

class ProjectContactOut(ProjectContactBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True

# --- Result Proofs ---
class ProjectResultProofBase(BaseModel):
    data_da_coleta: Optional[str] = Field(None, max_length=50)
    resultado: str = Field(..., max_length=200)

class ProjectResultProofCreate(ProjectResultProofBase):
    pass

class ProjectResultProofUpdate(BaseModel):
    data_da_coleta: Optional[str] = Field(None, max_length=50)
    resultado: Optional[str] = Field(None, max_length=200)

class ProjectResultProofOut(ProjectResultProofBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True

# --- CNMP Awards ---
class ProjectCnmpAwardBase(BaseModel):
    ano: str = Field(..., max_length=10)
    categoria: str = Field(..., max_length=100)

class ProjectCnmpAwardCreate(ProjectCnmpAwardBase):
    pass

class ProjectCnmpAwardUpdate(BaseModel):
    ano: Optional[str] = Field(None, max_length=10)
    categoria: Optional[str] = Field(None, max_length=100)

class ProjectCnmpAwardOut(ProjectCnmpAwardBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True
