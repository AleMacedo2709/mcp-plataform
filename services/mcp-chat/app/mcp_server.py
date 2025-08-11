from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any
from .db import search_projects, get_project
from .resources import search_in_resources
from .core.settings import settings

mcp = FastMCP()

@mcp.tool()
def query_project(term: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Buscar projetos por termo (nome/descrição) e retornar lista com id, nome, descrição e fase."""
    return search_projects(term, limit)

@mcp.tool()
def get_project_by_id(project_id: int) -> Dict[str, Any]:
    """Obter um projeto completo pelo ID."""
    p = get_project(project_id)
    return p or {}

@mcp.tool()
def search_resources(query: str, limit: int = 5) -> List[Dict[str, str]]:
    """Buscar trechos em arquivos de resources (txt/md/csv) por substring simples."""
    return search_in_resources(settings.RESOURCE_DIR, query, limit)

@mcp.tool()
def faq_campos_cnmp(nome_campo: str) -> str:
    """FAQ simplificada sobre os 29 campos do CNMP baseada em nomes conhecidos."""
    mapa = {
        "nome da iniciativa": "Título da iniciativa inscrita no Prêmio. Máx 300 caracteres.",
        "tipo de iniciativa": "Ação, Campanha, Ferramenta. Escolha única.",
        "classificação": "Origem ou vínculo institucional da iniciativa. Escolha única.",
        "fase de implementação": "Fase atual: parcial ou integral."
    }
    k = nome_campo.strip().lower()
    return mapa.get(k, "Campo não mapeado no FAQ DEV. Consulte o formulário para detalhes.")
