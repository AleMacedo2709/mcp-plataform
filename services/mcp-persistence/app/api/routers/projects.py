from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, File
from fastapi.responses import FileResponse
import logging
from sqlalchemy.orm import Session
from ...db.session import SessionLocal, init_db
from ...db import crud, models
from ...schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectOut,
    ProjectMemberCreate,
    ProjectMemberUpdate,
)
from ...security.deps import require_roles, get_current_user
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
    # Garantir owner vindo do header em DEV
    data = payload.model_dump()
    data['owner'] = request.headers.get('x-user') or data.get('owner') or 'unknown@local'
    project = crud.create_project(db, ProjectCreate(**data))
    # Prepara 'fase' compatível
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_de_implementacao
    log.info('project_created id=%s', out.id)
    await send_audit('project_created', {'id': out.id, 'nome': out.nome_da_iniciativa})
    log.info('project_updated id=%s', out.id)
    await send_audit('project_updated', {'id': out.id, 'nome': out.nome_da_iniciativa})
    return out

@router.get("/{project_id}/attachments")
def list_attachments(project_id: int):
    from ...db.session import SessionLocal
    from ...db.models import Attachment
    db = SessionLocal()
    try:
        rows = db.query(Attachment).filter(Attachment.project_id == project_id).order_by(Attachment.created_at.desc()).all()
        return [{
            'id': a.id,
            'project_id': a.project_id,
            'original_name': a.original_name,
            'stored_path': a.stored_path,
            'content_type': a.content_type,
            'size_bytes': a.size_bytes,
            'created_at': a.created_at.isoformat() if a.created_at else None,
        } for a in rows]
    finally:
        db.close()

@router.post("/{project_id}/attachments")
async def upload_attachment(project_id: int, request: Request, file: UploadFile = File(...)):
    import os, uuid, shutil
    uploads_root = os.getenv('UPLOAD_DIR', '/data/uploads')
    os.makedirs(uploads_root, exist_ok=True)
    # Estrutura: /data/uploads/{project_id}/
    target_dir = os.path.join(uploads_root, str(project_id))
    os.makedirs(target_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(target_dir, safe_name)
    # Write in chunks to support large files
    with open(dest, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    # Persist entry in DB (optional lightweight)
    try:
        from ...db.session import SessionLocal
        from ...db.models import Attachment
        db = SessionLocal()
        a = Attachment(
            project_id=project_id,
            original_name=file.filename,
            stored_path=f"/uploads/{project_id}/{safe_name}",
            content_type=getattr(file, 'content_type', None),
            size_bytes=os.path.getsize(dest)
        )
        db.add(a); db.commit(); db.refresh(a)
        logging.getLogger('mcp_persistence').info(
            'attachment_uploaded project_id=%s id=%s name=%s size=%s path=%s',
            project_id, a.id, a.original_name, a.size_bytes, a.stored_path
        )
        db.close()
    except Exception:
        pass
    return {"status": "ok", "path": f"/uploads/{project_id}/{safe_name}", "filename": file.filename, "size": os.path.getsize(dest)}


@router.get("/{project_id}/attachments/{attachment_id}/download")
def download_attachment(project_id: int, attachment_id: int):
    import os
    from ...db.session import SessionLocal
    from ...db.models import Attachment

    db = SessionLocal()
    try:
        a = db.query(Attachment).filter(Attachment.id == attachment_id, Attachment.project_id == project_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Anexo não encontrado")

        uploads_root = os.getenv('UPLOAD_DIR', '/data/uploads')
        # stored_path example: /uploads/{project_id}/{filename}
        try:
            _, rel = a.stored_path.split('/uploads', 1)
            disk_path = os.path.join(uploads_root, rel.lstrip('/'))
        except Exception:
            # fallback to conventional layout
            disk_path = os.path.join(uploads_root, str(project_id), os.path.basename(a.stored_path))

        if not os.path.exists(disk_path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado no servidor")

        filename = a.original_name or os.path.basename(disk_path)
        media_type = a.content_type or 'application/octet-stream'
        return FileResponse(path=disk_path, media_type=media_type, filename=filename)
    finally:
        db.close()


# --- Project Cover (Capa da iniciativa) ---
@router.post("/{project_id}/cover")
async def upload_project_cover(project_id: int, file: UploadFile = File(...)):
    import os, uuid
    uploads_root = os.getenv('UPLOAD_DIR', '/data/uploads')
    os.makedirs(uploads_root, exist_ok=True)
    target_dir = os.path.join(uploads_root, str(project_id), 'cover')
    os.makedirs(target_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(target_dir, safe_name)
    with open(dest, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    from ...db.session import SessionLocal
    from ...db.models import ProjectCover, Project
    db = SessionLocal()
    try:
        # Ensure project exists
        project = db.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail='Projeto não encontrado')

        # Remove previous cover (single cover policy)
        db.query(ProjectCover).filter(ProjectCover.project_id == project_id).delete()

        cover = ProjectCover(
            project_id=project_id,
            original_name=file.filename,
            stored_path=f"/uploads/{project_id}/cover/{safe_name}",
            content_type=getattr(file, 'content_type', None),
            size_bytes=os.path.getsize(dest)
        )
        db.add(cover)
        # Optional: update Project.capa_da_iniciativa for backward compatibility
        project.capa_da_iniciativa = cover.stored_path
        db.commit()
        db.refresh(cover)
        return {
            'id': cover.id,
            'project_id': cover.project_id,
            'original_name': cover.original_name,
            'stored_path': cover.stored_path,
            'content_type': cover.content_type,
            'size_bytes': cover.size_bytes
        }
    finally:
        db.close()


@router.get("/{project_id}/cover")
def get_project_cover(project_id: int):
    from ...db.session import SessionLocal
    from ...db.models import ProjectCover
    db = SessionLocal()
    try:
        cover = db.query(ProjectCover).filter(ProjectCover.project_id == project_id).order_by(ProjectCover.created_at.desc()).first()
        if not cover:
            raise HTTPException(status_code=404, detail='Capa não encontrada')
        return {
            'id': cover.id,
            'project_id': cover.project_id,
            'original_name': cover.original_name,
            'stored_path': cover.stored_path,
            'content_type': cover.content_type,
            'size_bytes': cover.size_bytes,
            'created_at': cover.created_at.isoformat() if cover.created_at else None
        }
    finally:
        db.close()


# --- Project Members (Equipe) ---
@router.get("/{project_id}/members")
def list_members(project_id: int, db: Session = Depends(get_db)):
    rows = crud.list_project_members(db, project_id)
    return [
        {"id": m.id, "project_id": m.project_id, "name": m.name, "email": m.email, "role": m.role, "created_at": m.created_at}
        for m in rows
    ]

@router.post("/{project_id}/members")
def add_member(project_id: int, payload: ProjectMemberCreate, db: Session = Depends(get_db)):
    if not payload.name or not payload.email:
        raise HTTPException(status_code=400, detail='Nome e email são obrigatórios')
    m = crud.add_project_member(db, project_id, payload)
    return {"id": m.id, "name": m.name, "email": m.email, "role": m.role}

@router.delete("/{project_id}/members/{member_id}")
def remove_member(project_id: int, member_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_project_member(db, project_id, member_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Membro não encontrado')
    return {"status":"deleted"}

@router.put("/{project_id}/members/{member_id}")
def update_member(project_id: int, member_id: int, payload: ProjectMemberUpdate, db: Session = Depends(get_db)):
    m = crud.update_project_member(db, project_id, member_id, payload)
    if not m:
        raise HTTPException(status_code=404, detail='Membro não encontrado')
    return {"id": m.id, "name": m.name, "email": m.email, "role": m.role}

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_de_implementacao
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
        # Permitir edição por membros do projeto
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros da equipe podem editar')
    project = crud.update_project(db, project_id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    out = ProjectOut.model_validate(project)
    out.fase = project.fase_de_implementacao
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
            "fase": p.fase_de_implementacao
        }
        projects.append(out)
    return {"projects": projects, "total": total}
