from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, desc, asc
from ..db import models
from ..schemas import ProjectCreate, ProjectUpdate

def create_project(db: Session, data: ProjectCreate) -> models.Project:
    project = models.Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project(db: Session, project_id: int) -> models.Project | None:
    return db.get(models.Project, project_id)

def delete_project(db: Session, project_id: int) -> bool:
    project = db.get(models.Project, project_id)
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True

def update_project(db: Session, project_id: int, data: ProjectUpdate) -> models.Project | None:
    project = db.get(models.Project, project_id)
    if not project:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(project, k, v)
    db.commit()
    db.refresh(project)
    return project

def list_projects(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    tipo_iniciativa: str | None = None,
    classificacao: str | None = None,
    fase: str | None = None,
    order_by: str | None = None,
    order: str | None = None
):
    q = select(models.Project)
    if search:
        like = f"%{search}%"
        q = q.where(or_(
            models.Project.nome_iniciativa.ilike(like),
            models.Project.descricao.ilike(like)
        ))
    if tipo_iniciativa:
        q = q.where(models.Project.tipo_iniciativa == tipo_iniciativa)
    if classificacao:
        q = q.where(models.Project.classificacao == classificacao)
    if fase:
        # compat: frontend usa 'fase' mas o campo é 'fase_implementacao'
        q = q.where(models.Project.fase_implementacao == fase)

    # Ordenação
    colmap = {
        "created_at": models.Project.created_at,
        "data_inicial_operacao": models.Project.data_inicial_operacao,
        "nome_iniciativa": models.Project.nome_iniciativa,
    }
    if order_by in colmap:
        col = colmap[order_by]
        q = q.order_by(desc(col) if (order or "").lower() == "desc" else asc(col))
    else:
        q = q.order_by(desc(models.Project.created_at))

    total = db.execute(select(func.count()).select_from(q.subquery())).scalar_one()
    rows = db.execute(q.offset(skip).limit(limit)).scalars().all()
    return rows, total
