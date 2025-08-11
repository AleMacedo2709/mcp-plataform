from fastapi import APIRouter, Depends, HTTPException, Query
import logging
from sqlalchemy.orm import Session
from ..db.session import SessionLocal, init_db
from ..db import crud, models
from ..schemas import ProjectCreate, ProjectUpdate, ProjectOut
from ..security.deps import require_roles, get_current_user
from packages.institutional.tools.audit import send_audit
from typing import Optional

router = APIRouter()
log = logging.getLogger('mcp_persistence')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializa tabelas no primeiro import/arranque
init_db()

@router.post("", response_model=ProjectOut)
async def create_project(request: Request, payload: ProjectCreate, db: Session = Depends(get_db), _: bool = Depends(require_roles('editor','admin'))):
    project = crud.create_project(db, payload)
    # Prepara 'fase' compatível
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_implementacao
    log.info('project_created id=%s', out.id)
    await send_audit('project_created', {'id': out.id, 'nome': out.nome_da_iniciativa}); log.info('project_updated id=%s', out.id)
    await send_audit('project_updated', {'id': out.id, 'nome': out.nome_da_iniciativa}); return out

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_implementacao
    return out

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    # owner check
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    roles = request.headers.get('x-role','') if request else ''
    roles = [r.strip() for r in roles.split(',') if r.strip()]
    user = get_current_user(request)
    if 'admin' not in roles and existing.owner != user:
        raise HTTPException(status_code=403, detail='Somente o proprietário pode editar')
    project = crud.update_project(db, project_id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_implementacao
    return out

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('admin'))):
    # owner check (admin já exigido, mas mantemos para logs)
    ok = crud.delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    log.info('project_deleted id=%s', project_id)
    await send_audit('project_deleted', {'id': project_id}); return {"status": "deleted"}

@router.get("")
def list_projects(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    tipo_iniciativa: Optional[str] = None,
    classificacao: Optional[str] = None,
    fase: Optional[str] = None,
    orderBy: Optional[str] = Query(None, alias="orderBy"),
    order: Optional[str] = None,
    db: Session = Depends(get_db),
):
    rows, total = crud.list_projects(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        tipo_iniciativa=tipo_iniciativa,
        classificacao=classificacao,
        fase=fase,
        order_by=orderBy,
        order=order
    )
    # compat response
    projects = []
    for p in rows:
        out = {
            **{k: getattr(p, k) for k in p.__dict__.keys() if not k.startswith("_")},
            "fase": p.fase_implementacao
        }
        projects.append(out)
    return {"projects": projects, "total": total}
