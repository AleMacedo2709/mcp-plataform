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
    ProjectActionCreate,
    ProjectActionUpdate,
    ProjectContactCreate,
    ProjectContactUpdate,
    ProjectResultProofCreate,
    ProjectResultProofUpdate,
    ProjectCnmpAwardCreate,
    ProjectCnmpAwardUpdate,
)
from ...security.deps import require_roles, get_current_user
from packages.institutional.tools.audit import send_audit
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])  # compat


def _scan_file_for_malware(path: str) -> bool:
    """Retorna True se o arquivo for seguro. Usa clamd se disponível; fallback para clamscan; caso indisponível, permite (fail-open)."""
    try:
        import os
        host = os.getenv('CLAMAV_HOST', 'clamav')
        port = int(os.getenv('CLAMAV_PORT', '3310'))
        try:
            import clamd
            cd = clamd.ClamdNetworkSocket(host=host, port=port)
            try:
                cd.ping()
            except Exception:
                cd = None
            if cd is not None:
                res = cd.scan(path)
                # {'/path': ('FOUND','MalwareName')} ou ('OK', None)
                status = list(res.values())[0][0] if isinstance(res, dict) and res else 'OK'
                return status == 'OK'
        except Exception:
            pass
        # Fallback para clamscan
        try:
            import subprocess
            r = subprocess.run(['clamscan', '--no-summary', path], capture_output=True, text=True)
            if r.returncode == 0:
                return True
            # returncode 1 = encontrado malware; 2 = erro
            return False
        except Exception:
            # Se não houver scanner disponível, fail-open (registro via log poderia ser adicionado)
            return True
    except Exception:
        return True
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
@limiter.limit("20/minute")
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
@limiter.limit("30/minute")
async def upload_attachment(project_id: int, request: Request, file: UploadFile = File(...), _: bool = Depends(require_roles('editor','admin'))):
    import os, uuid, shutil
    import filetype
    uploads_root = os.getenv('UPLOAD_DIR', '/data/uploads')
    os.makedirs(uploads_root, exist_ok=True)
    # Estrutura: /data/uploads/{project_id}/
    target_dir = os.path.join(uploads_root, str(project_id))
    os.makedirs(target_dir, exist_ok=True)
    # basic validation
    allowed_ext = {'.pdf', '.png', '.jpg', '.jpeg', '.docx', '.txt'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail='Extensão de arquivo não permitida')
    # limit size ~ 50MB
    max_bytes = 50 * 1024 * 1024
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(target_dir, safe_name)
    # Write in chunks to support large files
    with open(dest, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            if f.tell() > max_bytes:
                f.close(); os.remove(dest)
                raise HTTPException(status_code=413, detail='Arquivo excede o tamanho máximo permitido (50MB)')
    # validate magic/mime
    try:
        kind = filetype.guess(dest)
        if not kind:
            raise HTTPException(status_code=400, detail='Tipo de arquivo inválido')
        mime = kind.mime.lower()
        valid_mimes = {'application/pdf','image/png','image/jpeg','application/vnd.openxmlformats-officedocument.wordprocessingml.document','text/plain'}
        if mime not in valid_mimes:
            os.remove(dest)
            raise HTTPException(status_code=400, detail='MIME não permitido')
    except HTTPException:
        raise
    except Exception:
        os.remove(dest)
        raise HTTPException(status_code=400, detail='Falha ao validar arquivo')

    # Anti-malware (opcional, fail-open se indisponível)
    try:
        safe = _scan_file_for_malware(dest)
        if not safe:
            os.remove(dest)
            raise HTTPException(status_code=400, detail='Arquivo reprovado na varredura de malware')
    except HTTPException:
        raise
    except Exception:
        # se scanner falhar, manter upload mas poderíamos registrar
        pass
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
async def upload_project_cover(project_id: int, file: UploadFile = File(...), _: bool = Depends(require_roles('editor','admin'))):
    import os, uuid
    import filetype
    uploads_root = os.getenv('UPLOAD_DIR', '/data/uploads')
    os.makedirs(uploads_root, exist_ok=True)
    target_dir = os.path.join(uploads_root, str(project_id), 'cover')
    os.makedirs(target_dir, exist_ok=True)
    # only images for cover
    allowed_ext = {'.png', '.jpg', '.jpeg'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail='Capa deve ser imagem (png/jpg/jpeg)')
    max_bytes = 10 * 1024 * 1024
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(target_dir, safe_name)
    with open(dest, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            if f.tell() > max_bytes:
                f.close(); os.remove(dest)
                raise HTTPException(status_code=413, detail='Capa excede o tamanho máximo permitido (10MB)')
    try:
        kind = filetype.guess(dest)
        if not kind or kind.mime.lower() not in {'image/png','image/jpeg'}:
            os.remove(dest)
            raise HTTPException(status_code=400, detail='Capa deve ser imagem válida (png/jpg)')
    except HTTPException:
        raise
    except Exception:
        os.remove(dest)
        raise HTTPException(status_code=400, detail='Falha ao validar arquivo')

    # Anti-malware (opcional)
    try:
        safe = _scan_file_for_malware(dest)
        if not safe:
            os.remove(dest)
            raise HTTPException(status_code=400, detail='Imagem reprovada na varredura de malware')
    except HTTPException:
        raise
    except Exception:
        pass

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


# --- Project Actions ---
@router.get("/{project_id}/actions")
def list_actions(project_id: int, db: Session = Depends(get_db)):
    rows = crud.list_project_actions(db, project_id)
    return [
        {
            "id": a.id,
            "project_id": a.project_id,
            "descricao": a.descricao,
            "area_responsavel": a.area_responsavel,
            "email_responsavel": a.email_responsavel,
            "progresso": a.progresso,
            "inicio_previsto": a.inicio_previsto,
            "termino_previsto": a.termino_previsto,
            "inicio_efetivo": a.inicio_efetivo,
            "termino_efetivo": a.termino_efetivo,
            "created_at": a.created_at,
        }
        for a in rows
    ]

@router.post("/{project_id}/actions")
def add_action(project_id: int, payload: ProjectActionCreate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    # Permitir somente proprietário, admin ou membro da equipe
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros da equipe podem incluir ações')
    if not payload.descricao:
        raise HTTPException(status_code=400, detail='Descrição é obrigatória')
    a = crud.add_project_action(db, project_id, payload)
    return {"id": a.id}

@router.put("/{project_id}/actions/{action_id}")
def update_action(project_id: int, action_id: int, payload: ProjectActionUpdate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros da equipe podem editar ações')
    a = crud.update_project_action(db, project_id, action_id, payload)
    if not a:
        raise HTTPException(status_code=404, detail='Ação não encontrada')
    return {"status":"updated"}

@router.delete("/{project_id}/actions/{action_id}")
def delete_action(project_id: int, action_id: int, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros da equipe podem excluir ações')
    ok = crud.delete_project_action(db, project_id, action_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Ação não encontrada')
    return {"status":"deleted"}


# --- Project Contacts ---
@router.get("/{project_id}/contacts")
def list_contacts(project_id: int, db: Session = Depends(get_db)):
    rows = crud.list_project_contacts(db, project_id)
    return [{"id":c.id,"project_id":c.project_id,"nome":c.nome,"email":c.email,"created_at":c.created_at} for c in rows]

@router.post("/{project_id}/contacts")
def add_contact(project_id: int, payload: ProjectContactCreate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    if not payload.nome or not payload.email:
        raise HTTPException(status_code=400, detail='Nome e email são obrigatórios')
    # owner/admin/member
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros podem incluir contatos')
    c = crud.add_project_contact(db, project_id, payload)
    return {"id": c.id}

@router.put("/{project_id}/contacts/{contact_id}")
def update_contact(project_id: int, contact_id: int, payload: ProjectContactUpdate, db: Session = Depends(get_db)):
    c = crud.update_project_contact(db, project_id, contact_id, payload)
    if not c:
        raise HTTPException(status_code=404, detail='Contato não encontrado')
    return {"status": "updated"}

@router.delete("/{project_id}/contacts/{contact_id}")
def delete_contact(project_id: int, contact_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_project_contact(db, project_id, contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Contato não encontrado')
    return {"status": "deleted"}


# --- Project Result Proofs ---
@router.get("/{project_id}/results")
def list_results(project_id: int, db: Session = Depends(get_db)):
    rows = crud.list_project_results(db, project_id)
    return [{"id":r.id,"project_id":r.project_id,"data_da_coleta":r.data_da_coleta,"resultado":r.resultado,"created_at":r.created_at} for r in rows]

@router.post("/{project_id}/results")
def add_result(project_id: int, payload: ProjectResultProofCreate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    if not payload.resultado:
        raise HTTPException(status_code=400, detail='Resultado é obrigatório')
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros podem incluir comprovações')
    r = crud.add_project_result(db, project_id, payload)
    return {"id": r.id}

@router.put("/{project_id}/results/{result_id}")
def update_result(project_id: int, result_id: int, payload: ProjectResultProofUpdate, db: Session = Depends(get_db)):
    r = crud.update_project_result(db, project_id, result_id, payload)
    if not r:
        raise HTTPException(status_code=404, detail='Comprovação não encontrada')
    return {"status": "updated"}

@router.delete("/{project_id}/results/{result_id}")
def delete_result(project_id: int, result_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_project_result(db, project_id, result_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Comprovação não encontrada')
    return {"status": "deleted"}


# --- CNMP Awards ---
@router.get("/{project_id}/awards")
def list_awards(project_id: int, db: Session = Depends(get_db)):
    rows = crud.list_project_awards(db, project_id)
    return [{"id":a.id, "project_id":a.project_id, "ano":a.ano, "categoria":a.categoria, "created_at":a.created_at} for a in rows]

@router.post("/{project_id}/awards")
def add_award(project_id: int, payload: ProjectCnmpAwardCreate, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('editor','admin'))):
    if not payload.ano or not payload.categoria:
        raise HTTPException(status_code=400, detail='Ano e categoria são obrigatórios')
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    user = get_current_user(request)
    roles = [r.strip() for r in (request.headers.get('x-role','') or '').split(',') if r.strip()]
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros podem incluir prêmio')
    a = crud.add_project_award(db, project_id, payload)
    return {"id": a.id}

@router.put("/{project_id}/awards/{award_id}")
def update_award(project_id: int, award_id: int, payload: ProjectCnmpAwardUpdate, db: Session = Depends(get_db)):
    a = crud.update_project_award(db, project_id, award_id, payload)
    if not a:
        raise HTTPException(status_code=404, detail='Prêmio não encontrado')
    return {"status": "updated"}

@router.delete("/{project_id}/awards/{award_id}")
def delete_award(project_id: int, award_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_project_award(db, project_id, award_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Prêmio não encontrado')
    return {"status": "deleted"}

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
async def delete_project(project_id: int, db: Session = Depends(get_db), request: Request = None, _: bool = Depends(require_roles('admin','editor'))):
    # autoriza owner ou membro (admin também permitido)
    existing = crud.get_project(db, project_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Projeto não encontrado')
    roles = request.headers.get('x-role','') if request else ''
    roles = [r.strip() for r in roles.split(',') if r.strip()]
    user = get_current_user(request)
    if 'admin' not in roles and existing.owner != user:
        from ...db.models import ProjectMember
        is_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.email == user).first()
        if not is_member:
            raise HTTPException(status_code=403, detail='Somente o proprietário ou membros da equipe podem excluir')
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
    unidade_gestora: Optional[str] = None,
    selo: Optional[str] = None,
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
        unidade_gestora=unidade_gestora,
        selo=selo,
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


# --- Likes ---
@router.get("/{project_id}/likes")
def get_likes(project_id: int, db: Session = Depends(get_db)):
    total = crud.count_project_likes(db, project_id)
    return {"project_id": project_id, "likes": total}

@router.post("/{project_id}/likes")
def like(project_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)
    ok = crud.add_project_like(db, project_id, user or 'anon@local')
    return {"status": "ok", "liked": ok}
