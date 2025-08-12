from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, desc, asc
from ..db import models
from ..schemas import ProjectCreate, ProjectUpdate, ProjectMemberCreate, ProjectMemberUpdate

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
            models.Project.nome_da_iniciativa.ilike(like),
            models.Project.descricao.ilike(like)
        ))
    if tipo_iniciativa:
        q = q.where(models.Project.tipo_de_iniciativa == tipo_iniciativa)
    if classificacao:
        q = q.where(models.Project.classificacao == classificacao)
    if fase:
        # compat: frontend usa 'fase' mas o campo é 'fase_de_implementacao'
        q = q.where(models.Project.fase_de_implementacao == fase)

    # Ordenação
    colmap = {
        "created_at": models.Project.created_at,
        # Frontend uses 'data_inicial_operacao'; DB column is 'data_inicial_de_operacao'
        "data_inicial_operacao": models.Project.data_inicial_de_operacao,
        # Frontend uses 'nome_iniciativa'; DB column is 'nome_da_iniciativa'
        "nome_iniciativa": models.Project.nome_da_iniciativa,
    }
    if order_by in colmap:
        col = colmap[order_by]
        q = q.order_by(desc(col) if (order or "").lower() == "desc" else asc(col))
    else:
        q = q.order_by(desc(models.Project.created_at))

    total = db.execute(select(func.count()).select_from(q.subquery())).scalar_one()
    rows = db.execute(q.offset(skip).limit(limit)).scalars().all()
    return rows, total


# --- Project Members (Equipe) CRUD helpers ---
def list_project_members(db: Session, project_id: int):
    return db.query(models.ProjectMember).filter(models.ProjectMember.project_id == project_id).order_by(models.ProjectMember.created_at.desc()).all()

def add_project_member(db: Session, project_id: int, data: ProjectMemberCreate):
    member = models.ProjectMember(project_id=project_id, **data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def update_project_member(db: Session, project_id: int, member_id: int, data: ProjectMemberUpdate):
    m = db.get(models.ProjectMember, member_id)
    if not m or m.project_id != project_id:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return m

def delete_project_member(db: Session, project_id: int, member_id: int) -> bool:
    m = db.get(models.ProjectMember, member_id)
    if not m or m.project_id != project_id:
        return False
    db.delete(m)
    db.commit()
    return True
