"""
🤖 LLM Analyzer Service
======================

Serviço especializado para análise de texto com LLM.
Implementa o padrão "Contrato de Prompt Estruturado" conforme ADR 002.

Responsabilidades:
- Carregar contratos de prompt JSON
- Orquestrar contexto para LLM
- Garantir saída estruturada conforme schema
- Aplicar regras de negócio (maxLength)
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

from .schema_cnmp import load_specs
CSV_SCHEMA_PATH = os.getenv('CNMP_CSV_SCHEMA', '/app/mcp_ingestion/prompts/Formulario_CNMP_2025.csv')

class LLMAnalyzer:
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Inicializa o analisador LLM
        
        Args:
            prompts_dir: Diretório com contratos de prompt JSON
        """
        self.prompts_dir = Path(prompts_dir)
        self.prompts_cache = {}
        self._load_prompt_contracts()

    def _load_prompt_contracts(self):
        """
        🔧 Carrega contratos de prompt JSON
        
        Implementa ADR 002: Padrão "Contrato de Prompt Estruturado"
        """
        logger.info(f"📋 Carregando contratos de prompt de: {self.prompts_dir}")
        
        try:
            if not self.prompts_dir.exists():
                logger.warning(f"⚠️ Diretório de prompts não encontrado: {self.prompts_dir}")
                return
            
            for json_file in self.prompts_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        contract_data = json.load(f)
                    
                    # Validar estrutura do contrato
                    if not self._validate_contract_structure(contract_data):
                        logger.error(f"❌ Contrato inválido: {json_file.name}")
                        continue
                    
                    contract_name = contract_data["name"]
                    self.prompts_cache[contract_name] = contract_data
                    
                    logger.info(f"✅ Contrato carregado: {contract_name}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON inválido em {json_file.name}: {e}")
                except Exception as e:
                    logger.error(f"❌ Erro ao carregar {json_file.name}: {e}")
            
            logger.info(f"📋 {len(self.prompts_cache)} contratos carregados")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar contratos: {e}")

    def _validate_contract_structure(self, contract: Dict[str, Any]) -> bool:
        """Valida estrutura básica do contrato de prompt"""
        required_fields = ["name", "description", "system_prompt", "output_schema"]
        
        for field in required_fields:
            if field not in contract:
                logger.error(f"❌ Campo obrigatório ausente: {field}")
                return False
        
        # Validar schema structure
        schema = contract["output_schema"]
        if not isinstance(schema, dict) or "properties" not in schema:
            logger.error("❌ output_schema deve ter 'properties'")
            return False
        
        return True

    def analyze_with_llm(self, contract_name: str, extracted_text: str) -> Dict[str, Any]:
        """
        🎯 Análise principal com LLM
        
        Fluxo conforme PRD:
        1. Carregar contrato de prompt
        2. Montar contexto completo
        3. Enviar para LLM
        4. Validar resposta contra schema
        
        Args:
            contract_name: Nome do contrato de prompt
            extracted_text: Texto extraído do documento
            
        Returns:
            dict: Dados estruturados extraídos
        """
        logger.info(f"🤖 Iniciando análise com contrato: {contract_name}")
        
        try:
            # 1. Verificar se contrato existe
            if contract_name not in self.prompts_cache:
                available = list(self.prompts_cache.keys())
                raise ValueError(f"Contrato '{contract_name}' não encontrado. Disponíveis: {available}")
            
            contract = self.prompts_cache[contract_name]
            
            # 2. Montar prompt final
            final_prompt = self._build_final_prompt(contract, extracted_text)
            
            # 3. Chamar LLM
            response_text = self._call_llm(final_prompt)
            
            # 4. Processar resposta
            structured_data = self._process_llm_response(response_text, contract)
            
            # 5. Validar contra schema
            validated_data = self._validate_against_schema(structured_data, contract["output_schema"])
            
            logger.info(f"✅ Análise concluída: {len(validated_data)} campos extraídos")
            return validated_data
            
        except Exception as e:
            logger.error(f"❌ Erro na análise LLM: {e}")
            raise

    def _build_final_prompt(self, contract: Dict[str, Any], extracted_text: str) -> str:
        """
        🔧 Monta o prompt final conforme padrão estruturado
        
        Baseado na implementação otimizada de src/mcp_server/core/orchestrator.py
        Implementa as regras de negócio e limitações de campo
        """
        system_prompt = contract["system_prompt"]
        output_schema = contract["output_schema"]
        
        # Converter schema para formato legível (como no orchestrator original)
        output_instructions = json.dumps(output_schema, indent=2, ensure_ascii=False)
        
        # Regras de sumarização (conforme implementação original otimizada)
        summarization_rule = (
            "REGRAS IMPORTANTES:\n"
            "1. Sua saída DEVE ser um objeto JSON válido que adere estritamente ao SCHEMA JSON ESPERADO.\n"
            "2. Preste ATENÇÃO MÁXIMA à propriedade 'maxLength' em cada campo do schema.\n"
            "3. Se o texto extraído para um campo exceder o 'maxLength', você DEVE resumi-lo de forma concisa e precisa para se ajustar ao limite. Preserve o significado e a informação mais importante. NÃO TRUNCAR o texto no meio de uma frase."
        )
        
        # Template original do orchestrator (testado e funcional)
        final_prompt = f"""
{system_prompt}

{summarization_rule}

---
SCHEMA JSON ESPERADO:
{output_instructions}
---

Com base no CONTEÚDO DO DOCUMENTO abaixo, extraia as informações e gere o JSON de saída:

---
CONTEÚDO DO DOCUMENTO:
\"\"\"
{extracted_text}
\"\"\"
---

JSON DE SAÍDA:
"""
        
        return final_prompt

    def _call_llm(self, prompt: str) -> str:
        """Chama o provedor de LLM configurado"""
        from .llm_provider import call_llm_api
        
        try:
            logger.info("🌐 Enviando prompt para LLM...")
            response = call_llm_api(prompt)
            logger.info(f"✅ Resposta recebida: {len(response)} caracteres")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro na chamada LLM: {e}")
            raise

    def _process_llm_response(self, response_text: str, contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔍 Processa resposta do LLM
        
        Extrai JSON da resposta e trata possíveis problemas
        """
        try:
            # Tentar parsear JSON diretamente
            return json.loads(response_text.strip())
            
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Erro ao parsear JSON: {e}")
            
            # Tentar extrair JSON de resposta mal formatada
            cleaned_response = self._extract_json_from_text(response_text)
            
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.error(f"❌ Não foi possível extrair JSON válido")
                logger.error(f"Resposta original: {response_text[:500]}...")
                raise ValueError("LLM retornou resposta em formato inválido")

    def _extract_json_from_text(self, text: str) -> str:
        """Extrai JSON de texto que pode ter conteúdo extra"""
        import re
        
        # Procurar por JSON entre chaves
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group()
        
        # Se não encontrar, retornar texto original
        return text

    def _validate_against_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        ✅ Valida dados contra schema e aplica regras de negócio
        """
        validated_data = {}
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])
        
        # Validar campos obrigatórios
        for field in required_fields:
            if field not in data or not data[field]:
                logger.warning(f"⚠️ Campo obrigatório ausente: {field}")
                data[field] = "Não informado"
        
        # Validar propriedades
        for field_name, field_schema in properties.items():
            if field_name in data:
                value = data[field_name]
                
                # Aplicar maxLength
                max_length = field_schema.get("maxLength")
                if max_length and isinstance(value, str) and len(value) > max_length:
                    logger.warning(f"⚠️ Campo '{field_name}' excede maxLength ({len(value)} > {max_length})")
                    # Truncar preservando palavras
                    value = self._smart_truncate(value, max_length)
                
                validated_data[field_name] = value
        
        return validated_data

    def _smart_truncate(self, text: str, max_length: int) -> str:
        """
        🤖 Adequa texto usando IA para preservar essência e caber no limite
        
        Se o texto exceder o limite, usa LLM para resumir mantendo as
        informações principais do campo específico.
        """
        if len(text) <= max_length:
            return text
        
        # Se texto for muito pequeno para resumir, usar truncamento simples
        if max_length < 50:
            return self._simple_truncate(text, max_length)
        
        # Usar LLM para adequação inteligente
        try:
            return self._llm_smart_resize(text, max_length)
        except Exception as e:
            logger.warning(f"⚠️ Falha na adequação por IA: {e}. Usando truncamento simples.")
            return self._simple_truncate(text, max_length)
    
    def _simple_truncate(self, text: str, max_length: int) -> str:
        """Truncamento simples preservando palavras"""
        if len(text) <= max_length:
            return text
        
        # Truncar e encontrar último espaço
        truncated = text[:max_length - 3]  # -3 para "..."
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # Se o último espaço não está muito próximo do início
            return truncated[:last_space] + "..."
        else:
            return truncated + "..."
    
    def _llm_smart_resize(self, text: str, max_length: int) -> str:
        """
        🧠 Usa LLM para redimensionar texto preservando essência
        
        Args:
            text: Texto original que excede o limite
            max_length: Limite máximo de caracteres
            
        Returns:
            str: Texto adequado pela IA dentro do limite
        """
        # Calcular margem de segurança (10% menos que o limite)
        target_length = int(max_length * 0.9)
        
        # Prompt especializado para adequação de texto
        adequacao_prompt = f"""
TAREFA: Adequar texto para caber em {target_length} caracteres preservando a essência.

TEXTO ORIGINAL ({len(text)} caracteres):
{text}

INSTRUÇÕES:
1. Mantenha todas as informações ESSENCIAIS
2. Preserve números, datas, valores importantes
3. Use linguagem clara e concisa
4. NÃO adicione informações que não estão no texto original
5. Foque nas partes mais relevantes para um formulário oficial
6. RESULTADO DEVE TER NO MÁXIMO {target_length} caracteres

RESPOSTA (apenas o texto adequado, sem explicações):
"""
        
        try:
            # Usar o mesmo provedor LLM configurado
            from .llm_provider import call_llm_api
            
            logger.info(f"🤖 Adequando texto via IA: {len(text)} → {target_length} chars")
            
            # Fazer chamada para LLM com prompt específico
            adequated_text = call_llm_api(adequacao_prompt)
            
            # Limpar resposta (remover aspas, quebras extras, etc.)
            adequated_text = adequated_text.strip().strip('"').strip("'")
            
            # Verificar se resultado está dentro do limite
            if len(adequated_text) <= max_length:
                logger.info(f"✅ Texto adequado com sucesso: {len(adequated_text)} chars")
                return adequated_text
            else:
                logger.warning(f"⚠️ LLM retornou texto ainda longo ({len(adequated_text)}), truncando...")
                return self._simple_truncate(adequated_text, max_length)
                
        except Exception as e:
            logger.error(f"❌ Erro na adequação por IA: {e}")
            raise

    def list_available_prompts(self) -> list:
        """Lista contratos de prompt disponíveis"""
        return [
            {
                "name": name,
                "description": contract.get("description", ""),
                "output_fields": list(contract.get("output_schema", {}).get("properties", {}).keys())
            }
            for name, contract in self.prompts_cache.items()
        ]

    def get_prompt_contract(self, contract_name: str) -> Dict[str, Any]:
        """Retorna detalhes de um contrato específico"""
        if contract_name not in self.prompts_cache:
            raise ValueError(f"Contrato '{contract_name}' não encontrado")
        
        return self.prompts_cache[contract_name]

    def reload_contracts(self):
        """Recarrega contratos de prompt"""
        logger.info("🔄 Recarregando contratos de prompt...")
        self.prompts_cache.clear()
        self._load_prompt_contracts()

    def _validate_against_schema(self, data: dict) -> dict:
        """Override: valida usando CSV dinâmico se disponível."""
        import os
        specs = {}
        try:
            if os.path.exists(CSV_SCHEMA_PATH):
                specs = load_specs(CSV_SCHEMA_PATH)
        except Exception:
            specs = {}
        # fallback para validação existente, se definida
        validated = data.copy()
        if specs:
            for k, v in list(validated.items()):
                if k in specs:
                    max_len = specs[k].get('maxLength')
                    if isinstance(v, str) and max_len:
                        validated[k] = v[:max_len]
        return validated
