"""
📚 MCP Resources - Ingestion Server
===================================

MCP Resources para conhecimento sobre processamento de documentos.
Implementa o protocolo MCP oficial para fornecer contexto rico aos LLMs.

Conforme melhores práticas MCP: https://modelcontextprotocol.io/
"""

from typing import Dict, List, Any, Optional
from mcp import Server
from mcp.types import Resource, ResourceTemplate

# Inicializar MCP Server
mcp_server = Server("mcp-ingestion-server")

# =======================================================
# 📋 MCP RESOURCES - BASE DE CONHECIMENTO
# =======================================================

@mcp_server.list_resources()
async def list_resources() -> List[Resource]:
    """Lista todos os resources disponíveis no servidor de ingestão"""
    return [
        Resource(
            uri="ingestion://documents/supported-formats",
            name="Formatos de Documento Suportados",
            description="Lista completa de formatos suportados para análise",
            mimeType="application/json"
        ),
        Resource(
            uri="ingestion://processing/extraction-rules",
            name="Regras de Extração de Texto",
            description="Regras e padrões para extração de conteúdo estruturado",
            mimeType="application/json"
        ),
        Resource(
            uri="ingestion://llm/analysis-templates",
            name="Templates de Análise LLM",
            description="Templates e prompts para análise inteligente de documentos",
            mimeType="application/json"
        ),
        Resource(
            uri="ingestion://examples/cnmp-projects",
            name="Exemplos CNMP",
            description="Exemplos de projetos CNMP bem-sucedidos para referência",
            mimeType="application/json"
        ),
        Resource(
            uri="ingestion://guidelines/best-practices",
            name="Melhores Práticas",
            description="Guidelines para processamento otimizado de documentos",
            mimeType="text/markdown"
        )
    ]

@mcp_server.read_resource()
async def read_resource(uri: str) -> str:
    """Lê o conteúdo de um resource específico"""
    
    if uri == "ingestion://documents/supported-formats":
        return _get_supported_formats()
    elif uri == "ingestion://processing/extraction-rules":
        return _get_extraction_rules()
    elif uri == "ingestion://llm/analysis-templates":
        return _get_analysis_templates()
    elif uri == "ingestion://examples/cnmp-projects":
        return _get_cnmp_examples()
    elif uri == "ingestion://guidelines/best-practices":
        return _get_best_practices()
    else:
        raise ValueError(f"Resource não encontrado: {uri}")

# =======================================================
# 📄 IMPLEMENTAÇÃO DOS RESOURCES
# =======================================================

def _get_supported_formats() -> str:
    """Resource: Formatos de documento suportados"""
    return """{
  "supported_formats": {
    "pdf": {
      "extensions": [".pdf"],
      "max_size_mb": 100,
      "extraction_method": "marker-pdf",
      "features": ["text_extraction", "layout_preservation", "table_detection"]
    },
    "docx": {
      "extensions": [".docx"],
      "max_size_mb": 50,
      "extraction_method": "python-docx",
      "features": ["text_extraction", "metadata", "comments"]
    },
    "doc": {
      "extensions": [".doc"],
      "max_size_mb": 50,
      "extraction_method": "legacy_converter",
      "features": ["text_extraction"]
    }
  },
  "quality_metrics": {
    "pdf_accuracy": "95%",
    "docx_accuracy": "99%",
    "processing_speed": "~2s per MB"
  }
}"""

def _get_extraction_rules() -> str:
    """Resource: Regras de extração estruturada"""
    return """{
  "extraction_rules": {
    "project_identification": {
      "title_patterns": [
        "^PROJETO:",
        "^TÍTULO:",
        "^NOME DO PROJETO:"
      ],
      "weight": 10
    },
    "objective_patterns": [
      "OBJETIVO GERAL:",
      "FINALIDADE:",
      "PROPÓSITO:"
    ],
    "description_markers": [
      "DESCRIÇÃO:",
      "RESUMO:",
      "DETALHAMENTO:"
    ],
    "metadata_extraction": {
      "dates": "\\\\d{2}/\\\\d{2}/\\\\d{4}",
      "values": "R\\\\$ ?[0-9.,]+",
      "duration": "\\\\d+ (meses|anos|dias)"
    }
  },
  "text_preprocessing": {
    "normalize_whitespace": true,
    "remove_headers_footers": true,
    "preserve_structure": true
  }
}"""

def _get_analysis_templates() -> str:
    """Resource: Templates para análise LLM"""
    return """{
  "analysis_templates": {
    "cnmp_project_analysis": {
      "system_prompt": "Você é um especialista em análise de projetos do CNMP. Analise o documento e extraia informações estruturadas.",
      "user_template": "Analise este documento de projeto: {document_text}",
      "output_schema": {
        "titulo": "string",
        "objetivo_geral": "string",
        "descricao": "string",
        "justificativa": "string",
        "cronograma": "string"
      }
    },
    "legal_document_analysis": {
      "system_prompt": "Analise documentos jurídicos extraindo informações relevantes.",
      "focus_areas": ["normative_references", "legal_basis", "stakeholders"]
    }
  },
  "quality_controls": {
    "max_tokens": 4000,
    "temperature": 0.3,
    "validation_required": true
  }
}"""

def _get_cnmp_examples() -> str:
    """Resource: Exemplos de projetos CNMP"""
    return """{
  "cnmp_examples": {
    "projeto_inovacao_digital": {
      "titulo": "Digitalização de Processos Administrativos",
      "categoria": "Inovação Tecnológica",
      "objetivo": "Modernizar fluxos de trabalho através de automação",
      "impact_score": 9.2,
      "lessons_learned": [
        "Importância do treinamento de usuários",
        "Necessidade de piloto antes da implementação completa"
      ]
    },
    "projeto_capacitacao": {
      "titulo": "Programa de Capacitação Continuada",
      "categoria": "Desenvolvimento Humano",
      "objetivo": "Aprimorar competências técnicas dos servidores",
      "impact_score": 8.7,
      "best_practices": [
        "Avaliação de necessidades prévia",
        "Metodologias ativas de aprendizagem"
      ]
    }
  },
  "success_patterns": {
    "clear_objectives": "Objetivos específicos e mensuráveis",
    "stakeholder_engagement": "Envolvimento das partes interessadas",
    "phased_implementation": "Implementação em fases"
  }
}"""

def _get_best_practices() -> str:
    """Resource: Melhores práticas em markdown"""
    return """# 🎯 Melhores Práticas - Processamento de Documentos

## 📋 Preparação de Documentos

### ✅ Formatos Recomendados
- **PDF**: Use PDFs com texto pesquisável (não escaneado)
- **DOCX**: Formato nativo do Word mais recente
- **Estrutura**: Mantenha hierarquia clara com títulos e subtítulos

### 📏 Limitações Técnicas
- **Tamanho máximo**: 100MB para PDFs, 50MB para DOCX
- **Páginas**: Máximo 500 páginas por documento
- **Qualidade**: PDFs com resolução mínima de 150 DPI

## 🤖 Otimização para Análise LLM

### 🎯 Estruturação de Conteúdo
1. **Títulos claros**: Use hierarquia H1, H2, H3
2. **Parágrafos concisos**: Máximo 200 palavras por parágrafo
3. **Listas organizadas**: Use bullet points para enumerações

### 🔍 Palavras-chave Importantes
- Inclua termos específicos do domínio (CNMP, MP, etc.)
- Use vocabulário padronizado da instituição
- Evite jargões muito técnicos sem explicação

## ⚡ Performance e Qualidade

### 📊 Métricas de Sucesso
- **Precisão de extração**: >95% para textos estruturados
- **Tempo de processamento**: <3 segundos por MB
- **Taxa de erro**: <2% em documentos bem formatados

### 🔧 Troubleshooting
- **Texto cortado**: Verifique se o PDF não está protegido
- **Formatação perdida**: Use DOCX em vez de DOC legado
- **Análise incompleta**: Divida documentos muito longos
"""

# =======================================================
# 🛠️ MCP TOOLS - FUNCIONALIDADES ESPECÍFICAS
# =======================================================

@mcp_server.list_tools()
async def list_tools():
    """Lista ferramentas disponíveis no servidor"""
    return [
        {
            "name": "analyze_document_structure",
            "description": "Analisa a estrutura de um documento e sugere melhorias",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "document_content": {"type": "string"},
                    "analysis_type": {"type": "string", "enum": ["basic", "detailed", "cnmp"]}
                }
            }
        },
        {
            "name": "validate_cnmp_compliance",
            "description": "Valida se um documento atende aos requisitos CNMP",
            "inputSchema": {
                "type": "object", 
                "properties": {
                    "project_data": {"type": "object"},
                    "validation_level": {"type": "string", "enum": ["basic", "strict"]}
                }
            }
        }
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Executa uma ferramenta específica"""
    
    if name == "analyze_document_structure":
        return await _analyze_document_structure(arguments)
    elif name == "validate_cnmp_compliance":
        return await _validate_cnmp_compliance(arguments)
    else:
        raise ValueError(f"Tool não encontrada: {name}")

async def _analyze_document_structure(args: Dict[str, Any]) -> Dict[str, Any]:
    """Tool: Analisa estrutura do documento"""
    content = args.get("document_content", "")
    analysis_type = args.get("analysis_type", "basic")
    
    # Análise básica da estrutura
    analysis = {
        "word_count": len(content.split()),
        "paragraph_count": content.count('\n\n') + 1,
        "has_titles": any(line.isupper() for line in content.split('\n')),
        "structure_quality": "good" if len(content.split()) > 100 else "needs_improvement"
    }
    
    if analysis_type == "detailed":
        analysis.update({
            "readability_score": _calculate_readability(content),
            "keyword_density": _analyze_keywords(content),
            "suggestions": _generate_suggestions(content)
        })
    
    return analysis

async def _validate_cnmp_compliance(args: Dict[str, Any]) -> Dict[str, Any]:
    """Tool: Valida conformidade CNMP"""
    project_data = args.get("project_data", {})
    validation_level = args.get("validation_level", "basic")
    
    required_fields = [
        "titulo", "objetivo_geral", "descricao", "justificativa",
        "cronograma", "recursos_necessarios"
    ]
    
    validation = {
        "is_compliant": all(field in project_data for field in required_fields),
        "missing_fields": [field for field in required_fields if field not in project_data],
        "completeness_score": len([f for f in required_fields if f in project_data]) / len(required_fields)
    }
    
    if validation_level == "strict":
        validation.update({
            "field_quality": _assess_field_quality(project_data),
            "recommendations": _generate_compliance_recommendations(project_data)
        })
    
    return validation

def _calculate_readability(text: str) -> float:
    """Calcula score de legibilidade"""
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    if sentences == 0:
        return 0.0
    avg_words_per_sentence = words / sentences
    return max(0, min(10, 10 - (avg_words_per_sentence - 15) / 5))

def _analyze_keywords(text: str) -> Dict[str, int]:
    """Analisa densidade de palavras-chave"""
    keywords = ["projeto", "objetivo", "cnmp", "ministério", "público"]
    return {kw: text.lower().count(kw) for kw in keywords}

def _generate_suggestions(text: str) -> List[str]:
    """Gera sugestões de melhoria"""
    suggestions = []
    if len(text.split()) < 200:
        suggestions.append("Documento muito curto - considere adicionar mais detalhes")
    if not any(char.isupper() for char in text):
        suggestions.append("Adicione títulos em maiúscula para melhor estruturação")
    return suggestions

def _assess_field_quality(data: Dict[str, Any]) -> Dict[str, str]:
    """Avalia qualidade dos campos"""
    quality = {}
    for field, value in data.items():
        if isinstance(value, str):
            if len(value) < 10:
                quality[field] = "too_short"
            elif len(value) > 1000:
                quality[field] = "too_long"
            else:
                quality[field] = "good"
    return quality

def _generate_compliance_recommendations(data: Dict[str, Any]) -> List[str]:
    """Gera recomendações de conformidade"""
    recommendations = []
    
    if "titulo" in data and len(data["titulo"]) < 10:
        recommendations.append("Título muito curto - seja mais descritivo")
    
    if "objetivo_geral" in data and "específico" not in data["objetivo_geral"].lower():
        recommendations.append("Objetivo geral deve ser mais específico e mensurável")
        
    return recommendations

# Exportar o servidor MCP para uso em outros módulos
__all__ = ["mcp_server"]
