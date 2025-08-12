from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ...db.session import SessionLocal
from ...db.models import Project

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Project)) or 0

    # Em andamento = fase_implementacao 'Implementação parcial'
    in_progress = db.scalar(
        select(func.count()).where(Project.fase_de_implementacao == "Implementação parcial")
    ) or 0
    # Concluídos = 'Implementação integral'
    completed = db.scalar(
        select(func.count()).where(Project.fase_de_implementacao == "Implementação integral")
    ) or 0

    # Documentos processados (placeholder em DEV)
    documentsProcessed = total  # Ajuste quando houver trilhas de upload

    return {
        "totalProjects": int(total),
        "projectsInProgress": int(in_progress),
        "projectsCompleted": int(completed),
        "documentsProcessed": int(documentsProcessed)
    }
