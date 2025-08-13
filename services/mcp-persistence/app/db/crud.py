from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, desc, asc
from ..db import models
from ..schemas import ProjectCreate, ProjectUpdate, ProjectMemberCreate, ProjectMemberUpdate, ProjectActionCreate, ProjectActionUpdate, ProjectContactCreate, ProjectContactUpdate, ProjectResultProofCreate, ProjectResultProofUpdate, ProjectCnmpAwardCreate, ProjectCnmpAwardUpdate

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
    unidade_gestora: str | None = None,
    selo: str | None = None,
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
    if unidade_gestora:
        q = q.where(models.Project.unidade_gestora.ilike(f"%{unidade_gestora}%"))
    if selo:
        q = q.where(models.Project.selo == selo)

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


# --- Project Actions CRUD helpers ---
def list_project_actions(db: Session, project_id: int):
    return db.query(models.ProjectAction).filter(models.ProjectAction.project_id == project_id).order_by(models.ProjectAction.created_at.desc()).all()

def add_project_action(db: Session, project_id: int, data: ProjectActionCreate):
    action = models.ProjectAction(project_id=project_id, **data.model_dump())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

def update_project_action(db: Session, project_id: int, action_id: int, data: ProjectActionUpdate):
    a = db.get(models.ProjectAction, action_id)
    if not a or a.project_id != project_id:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    db.commit()
    db.refresh(a)
    return a

def delete_project_action(db: Session, project_id: int, action_id: int) -> bool:
    a = db.get(models.ProjectAction, action_id)
    if not a or a.project_id != project_id:
        return False
    db.delete(a)
    db.commit()
    return True


# --- Likes helpers ---
def count_project_likes(db: Session, project_id: int) -> int:
    return db.query(models.ProjectLike).filter(models.ProjectLike.project_id == project_id).count()

def add_project_like(db: Session, project_id: int, user_email: str) -> bool:
    # Prevent duplicate like by same user
    exists = db.query(models.ProjectLike).filter(models.ProjectLike.project_id == project_id, models.ProjectLike.user_email == user_email).first()
    if exists:
        return False
    like = models.ProjectLike(project_id=project_id, user_email=user_email)
    db.add(like)
    db.commit()
    return True


# --- Contacts helpers ---
def list_project_contacts(db: Session, project_id: int):
    return db.query(models.ProjectContact).filter(models.ProjectContact.project_id == project_id).order_by(models.ProjectContact.created_at.desc()).all()

def add_project_contact(db: Session, project_id: int, data: ProjectContactCreate):
    c = models.ProjectContact(project_id=project_id, **data.model_dump())
    db.add(c)
    db.commit(); db.refresh(c)
    return c

def update_project_contact(db: Session, project_id: int, contact_id: int, data: ProjectContactUpdate):
    c = db.get(models.ProjectContact, contact_id)
    if not c or c.project_id != project_id:
        return None
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

def delete_project_contact(db: Session, project_id: int, contact_id: int) -> bool:
    c = db.get(models.ProjectContact, contact_id)
    if not c or c.project_id != project_id:
        return False
    db.delete(c); db.commit(); return True


# --- Result proofs helpers ---
def list_project_results(db: Session, project_id: int):
    return db.query(models.ProjectResultProof).filter(models.ProjectResultProof.project_id == project_id).order_by(models.ProjectResultProof.created_at.desc()).all()

def add_project_result(db: Session, project_id: int, data: ProjectResultProofCreate):
    r = models.ProjectResultProof(project_id=project_id, **data.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return r

def update_project_result(db: Session, project_id: int, result_id: int, data: ProjectResultProofUpdate):
    r = db.get(models.ProjectResultProof, result_id)
    if not r or r.project_id != project_id:
        return None
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit(); db.refresh(r)
    return r

def delete_project_result(db: Session, project_id: int, result_id: int) -> bool:
    r = db.get(models.ProjectResultProof, result_id)
    if not r or r.project_id != project_id:
        return False
    db.delete(r); db.commit(); return True


# --- CNMP Awards helpers ---
def list_project_awards(db: Session, project_id: int):
    return db.query(models.ProjectCnmpAward).filter(models.ProjectCnmpAward.project_id == project_id).order_by(models.ProjectCnmpAward.created_at.desc()).all()

def add_project_award(db: Session, project_id: int, data: ProjectCnmpAwardCreate):
    a = models.ProjectCnmpAward(project_id=project_id, **data.model_dump())
    db.add(a); db.commit(); db.refresh(a)
    return a

def update_project_award(db: Session, project_id: int, award_id: int, data: ProjectCnmpAwardUpdate):
    a = db.get(models.ProjectCnmpAward, award_id)
    if not a or a.project_id != project_id:
        return None
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    db.commit(); db.refresh(a)
    return a

def delete_project_award(db: Session, project_id: int, award_id: int) -> bool:
    a = db.get(models.ProjectCnmpAward, award_id)
    if not a or a.project_id != project_id:
        return False
    db.delete(a); db.commit(); return True
