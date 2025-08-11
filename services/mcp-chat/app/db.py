from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .core.settings import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def search_projects(term: str, limit: int = 5):
    with engine.connect() as conn:
        q = text("""
            SELECT id, nome_da_iniciativa, descricao, fase_de_implementacao
            FROM projects
            WHERE nome_da_iniciativa ILIKE :t OR descricao ILIKE :t
            ORDER BY id DESC
            LIMIT :l
        """)
        res = conn.execute(q, {"t": f"%{term}%", "l": limit}).mappings().all()
        return [dict(r) for r in res]

def get_project(pid: int):
    with engine.connect() as conn:
        q = text("""
            SELECT * FROM projects WHERE id = :id
        """)
        r = conn.execute(q, {"id": pid}).mappings().first()
        return dict(r) if r else None
