"""
🌐 LLM Provider Service
======================

Serviço para comunicação com provedores de LLM.
Reutiliza a lógica existente do projeto original.

Suporta múltiplos provedores conforme requisitos do PRD:
- Azure OpenAI
- OpenAI
- OpenRouter
"""

import os
import httpx
from openai import AzureOpenAI, OpenAI
import logging

logger = logging.getLogger(__name__)

def call_llm_api(final_prompt: str) -> str:
    """
    🌐 Conecta-se a um provedor de LLM baseado na configuração
    
    Implementação baseada na versão otimizada de src/mcp_server/services/llm_service.py
    """
    # Verificar se há chaves de API configuradas
    azure_key = os.getenv('AZURE_OPENAI_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    
    if not any([azure_key, openai_key, openrouter_key]):
        logger.warning("⚠️ Nenhuma chave de API configurada. Retornando dados de demonstração.")
        return _create_demo_response()
    
    provider = os.getenv("LLM_PROVIDER", "openrouter").lower()
    logger.info(f"🤖 Orquestração de Contexto - Provedor: {provider}")
    
    # Configuração SSL (False para desenvolvimento, True para produção)
    ssl_verify = os.getenv("SSL_VERIFY", "true").lower() == "true"
    http_client = httpx.Client(verify=ssl_verify)

    try:
        client = None
        model_name = ""

        if provider == "azure":
            # Azure OpenAI
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            
            if not all([api_key, azure_endpoint, model_name]):
                raise ValueError("Credenciais do Azure não configuradas no .env")
            
            client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-01",
                azure_endpoint=azure_endpoint,
                http_client=http_client
            )

        elif provider == "openai":
            # OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
            
            if not api_key:
                raise ValueError("Credencial OPENAI_API_KEY não configurada no .env")
            
            client = OpenAI(api_key=api_key, http_client=http_client)

        elif provider == "openrouter":
            # OpenRouter  
            api_key = os.getenv("OPENROUTER_API_KEY")
            model_name = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
            
            if not api_key:
                raise ValueError("Credencial OPENROUTER_API_KEY não configurada no .env")
            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                http_client=http_client
            )

        else:
            raise ValueError(f"Provedor de LLM '{provider}' não suportado.")

        # Fazer chamada para o LLM
        logger.info(f"📤 Enviando prompt para modelo '{model_name}' via {provider}...")
        
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},  # Força resposta JSON
            messages=[
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.1,  # Baixa temperatura para consistência
            max_tokens=4000,
            timeout=60
        )

        json_response = response.choices[0].message.content.strip()
        
        logger.info("🎉 Resposta da IA recebida com sucesso!")
        return json_response

    except Exception as e:
        logger.error(f"❌ Erro ao chamar API do provedor {provider}: {e}")
        raise
    finally:
        if http_client:
            http_client.close()


def _create_demo_response() -> str:
    """
    🎭 Cria resposta de demonstração quando não há chaves de API
    
    Retorna dados realistas para mostrar a funcionalidade do sistema
    """
    import json
    
    demo_data = {
        "nome_iniciativa": "Sistema Inteligente de Análise de Documentos - DEMONSTRAÇÃO",
        "tipo_iniciativa": "Modernização Tecnológica",
        "classificacao": "Eficiência Administrativa",
        "natureza_iniciativa": "Sistema de IA para análise automatizada",
        "iniciativa_vinculada": "Modernização Digital MP",
        "objetivo_estrategico_pen_mp": "Modernização e Eficiência",
        "programa_pen_mp": ["Gestão da Inovação", "Tecnologia da Informação"],
        "promocao_objetivo_estrategico": "Implementação de IA para automatizar análise de documentos",
        "data_inicial_operacao": "2025-01-01",
        "fase_implementacao": "Teste/Piloto",
        "descricao": "Sistema de demonstração que utiliza inteligência artificial para análise automatizada de documentos institucionais, extraindo informações estruturadas e preenchendo formulários automaticamente.",
        "estimativa_recursos": "R$ 150.000 (estimativa para demonstração)",
        "publico_impactado": "Servidores do MP-SP, cidadãos beneficiados pela eficiência",
        "orgaos_envolvidos": "MP-SP, Departamento de TI, Coordenadoria de Gestão Estratégica",
        "contatos": "Coordenador de Inovação - inovacao@mp.sp.gov.br",
        "desafio_1": "Automatizar processo manual de análise de documentos",
        "desafio_2": "Reduzir tempo de processamento de formulários",
        "desafio_3": "Melhorar precisão na extração de dados",
        "resolutividade": "Sistema permite processar documentos 10x mais rápido que processo manual",
        "inovacao": "Primeira implementação de IA para análise de documentos no MP-SP",
        "transparencia": "Relatórios automáticos sobre processamento e resultados gerados",
        "proatividade": "Sistema identifica padrões e sugere melhorias nos processos",
        "cooperacao": "Integração com sistemas existentes e treinamento de equipes",
        "resultado_1": "Redução de 80% no tempo de análise de documentos",
        "resultado_2": "Aumento de 95% na precisão da extração de dados",
        "resultado_3": "Melhoria na satisfação dos usuários em 90%",
        "categoria": "Tecnologia e Inovação"
    }
    
    logger.info("🎭 Retornando dados de demonstração (chaves de API não configuradas)")
    return json.dumps(demo_data, ensure_ascii=False, indent=2)

# Unified provider delegation (if available)
try:
    from packages.institutional.ia.provider import generate_json as unified_generate_json
except Exception:
    unified_generate_json = None


async def generate_json_via_unified(prompt: str, model: str, response_format: dict | None):
    if unified_generate_json:
        return await unified_generate_json(prompt, model, response_format)
    # fallback to existing provider logic if any (demo or openai client)
    try:
        return await create_response_json(prompt, model=model, response_format=response_format)  # type: ignore
    except Exception:
        return {"error": "No provider available"}
