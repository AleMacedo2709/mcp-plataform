from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    owner: str | None = Field(None, max_length=320)  # preenchido no backend
    nome_da_iniciativa: str = Field(..., max_length=300)
    tipo_de_iniciativa: str | None = Field(None, max_length=300)
    classificacao: str | None = Field(None, max_length=300)
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
    contatos: str | None = Field(None, max_length=300)
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
    comprovacao_dos_resultados: str | None = Field(None, max_length=300)
    capa_da_iniciativa: str | None = Field(None, max_length=300)
    categoria: str | None = Field(None, max_length=300)

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
