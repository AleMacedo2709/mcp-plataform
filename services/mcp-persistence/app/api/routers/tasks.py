from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.session import get_db
from ...db.models import Task
from ...schemas import TaskOut
from ...security.deps import get_current_user, require_roles
import logging, json

router = APIRouter()
log = logging.getLogger('mcp_persistence')

@router.post("", response_model=TaskOut)
def create_task(payload: dict, request: Request, db: Session = Depends(get_db)):
    # payload: {id,type,filename,owner,status}
    tid = payload.get("id")
    if not tid:
        raise HTTPException(400, "task id ausente")
    t = Task(
        id = tid,
        type = payload.get("type") or "unknown",
        filename = payload.get("filename"),
        owner = payload.get("owner") or (request.headers.get("x-user") or "unknown@local"),
        status = payload.get("status") or "queued",
        result = payload.get("result")
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    log.info("task_created id=%s type=%s", t.id, t.type)
    return t

@router.get("", response_model=List[TaskOut])
def list_tasks(owner: Optional[str] = None, skip: int = 0, limit: int = 50, request: Request = None, db: Session = Depends(get_db)):
    user = get_current_user(request)
    q = db.query(Task)
    if owner == "me" or (owner is None and request is not None):
        q = q.filter(Task.owner == user)
    elif owner:
        q = q.filter(Task.owner == owner)
    q = q.order_by(Task.created_at.desc())
    return q.offset(skip).limit(min(limit, 200)).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: str, request: Request, db: Session = Depends(get_db)):
    t = db.query(Task).filter(Task.id==task_id).first()
    if not t:
        raise HTTPException(404, "Task não encontrada")
    user = get_current_user(request)
    roles = request.headers.get('x-role','')
    roles = [r.strip() for r in roles.split(',') if r.strip()]
    if t.owner != user and "admin" not in roles:
        raise HTTPException(403, "Acesso negado")
    return t

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: str, payload: dict, request: Request, db: Session = Depends(get_db)):
    t = db.query(Task).filter(Task.id==task_id).first()
    if not t:
        raise HTTPException(404, "Task não encontrada")
    # Permitir que o owner altere status/result; admin sempre pode
    user = get_current_user(request)
    roles = request.headers.get('x-role','')
    roles = [r.strip() for r in roles.split(',') if r.strip()]
    if t.owner != user and "admin" not in roles:
        raise HTTPException(403, "Acesso negado")
    if "status" in payload: t.status = payload["status"]
    if "result" in payload: t.result = payload["result"] if isinstance(payload["result"], str) else json.dumps(payload["result"], ensure_ascii=False)
    db.commit(); db.refresh(t)
    log.info("task_updated id=%s status=%s", t.id, t.status)
    return t
