"""
Módulo com definições de IA
"""

import logging
import os
from typing import Any

import openai
import tiktoken
from dotenv import load_dotenv
from flask import current_app
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    wait_chain,
    wait_fixed,
)

from ania import config

logger = logging.getLogger(name=__name__)

# ---------------------------------------------------------
# Configuração - Microsoft Azure OpenAI
# load_dotenv()

# Lê diretamente das variáveis de ambiente
openai.api_type = config.OPENAI_API_TYPE
openai.api_version = config.OPENAI_API_VERSION
openai.api_base = config.OPENAI_API_BASE
openai.api_key = config.OPENAI_API_KEY

# Lê das variáveis de ambiente e, eventualmente, da Vault
# openai.api_type = config.Config.API_TYPE
# openai.api_version = config.Config.API_VERSION
# openai_endpoint, openai_key = obter_dados_acesso_open_ai(app.config)
# openai.api_base = openai_endpoint
# openai.api_key = openai_key


if openai.api_base is None:
    raise Exception('A variável de ambiente API_BASE não foi definida')
if openai.api_key is None:
    raise Exception('A variável de ambiente API_KEY não foi definida')
if openai.api_type is None:
    raise Exception('A variável de ambiente API_TYPE não foi definida')
if openai.api_version is None:
    raise Exception('A variável de ambiente API_VERSION não foi definida')


@retry(
    wait=wait_chain(
        *[wait_random_exponential(min=2, max=5) for i in range(3)]
        + [wait_fixed(15)]
    ),
    stop=stop_after_attempt(max_attempt_number=8),
)
def criar_embedding(
    texto: str, engine: str = 'text-embedding-ada-002'
) -> tuple[Any, int]:
    """
    Cria os *embeddings* a partir do texto..

    Engine: tce-ada (Microsoft Azure) ou text-embedding-ada-002 (OpenAI)
    FIXME: Aqui dá erro... decompor função...
    :param texto:
    :param engine:
    :return:
    """
    logger.debug('Inicio dos embeddings')

    # Faz o encoding e decode
    try:
        texto = texto.encode(encoding='utf-8', errors='ignore').decode()
        texto = texto.replace('\n', ' ')

    except Exception as e:
        raise Exception('Erro para o encoding ou decode do texto') from e

    # Cria o Embedding
    try:
        response = openai.Embedding.create(input=[texto], engine=engine)
        embedding_ania = response['data'][0]['embedding']
        total_tokens = response['usage']['total_tokens']
        logger.info('Embedding - %s tokens', total_tokens)
        return embedding_ania, total_tokens

    except Exception as e:
        logger.error('Erro ao obter o embedding:', e)
        raise Exception('Erro para o envio de tokens') from e


def completion(prompt: str, historico, modelo_gpt: str, max_tokens: int = 500):
    """
    sss

    :param prompt:
    :param historico:
    :param modelo_gpt:
    :param max_tokens:
    :return:
    """
    if modelo_gpt == 'gpt-3.5-turbo-16k':
        engine = current_app.config['MODEL_GPT35_TURBO_16K']
        limite_tokens = 16385

    elif modelo_gpt == 'gpt-4o':
        engine = current_app.config['MODEL_GPT4O']
        limite_tokens = 128000

    else:
        engine = current_app.config['MODEL_GPT35_TURBO']
        limite_tokens = 4096

    logger.info(
        'Modelo GPT definido "%s", resultando em %s limite_tokens',
        modelo_gpt,
        limite_tokens,
    )

    prompt = prompt.encode(encoding='utf-8', errors='ignore').decode()

    # mensagens = [] # Não está sendo utilizado em nada
    mensagens = obter_mensagens(prompt=prompt, historico=historico)

    # Calcula o número de tokens
    num_tokens_prompt = num_tokens_from_messages(mensagens)
    logger.debug('O valor para "num_tokens_prompt" é "%s"', num_tokens_prompt)
    logger.debug('O valor para "max_tokens" é "%s"', max_tokens)
    logger.debug('O valor para "limite_tokens" é "%s"', limite_tokens)
    logger.debug('O comprimento de "historico" é "%s"', len(historico))

    # Ajustes para não ultrapassar o limite de tokens
    if ((num_tokens_prompt + max_tokens) > limite_tokens) and len(
        historico
    ) > 10:
        logger.debug('Removendo parte do histórico')
        mensagens = obter_mensagens(prompt=prompt, historico=historico[-6:])
        num_tokens_prompt = num_tokens_from_messages(messages=mensagens)

    while (num_tokens_prompt + max_tokens) > limite_tokens:
        logger.debug('Removendo final do texto. Tokens: %s', num_tokens_prompt)
        mensagens[-1]['content'] = mensagens[-1]['content'][:-300]
        num_tokens_prompt = num_tokens_from_messages(messages=mensagens)

    try:
        response = openai.ChatCompletion.create(
            messages=mensagens,
            temperature=0.1,
            engine=engine,  # Microsoft Azure
            # model="gpt-3.5-turbo", #OpenAI
            # max_tokens = max_tokens,
            stream=True,
        )

        # Dados retornados quando stream=False
        # total_tokens = response['usage']['total_tokens']
        # logger.info('total_tokens: %s', type(total_tokens))
        logger.info('Cheguei ao final.... %s', num_tokens_prompt)
        return response, num_tokens_prompt

    except Exception as ex:
        logger.error('Erro - OpenAI back:', ex)
        return ('Erro - OpenAI back: %s' % ex), 0


def obter_mensagens(prompt, historico) -> list:
    """
    Obtêm as mensagens que estão no chat?

    :param prompt:
    :param historico:
    :return:
    """
    logger.info('Obtêm as mensagens que estão no chat?')
    mensagens = []

    # Contexto da conversa (mensagens anteriores)
    mensagens_anteriores = []

    if historico:
        for registro in historico[-12:]:
            if registro['tipo'] == 'enviada':
                mensagens_anteriores.append(
                    {'role': 'user', 'content': registro['mensagem']}
                )

            elif registro['tipo'] == 'recebida':
                mensagens_anteriores.append(
                    {'role': 'assistant', 'content': registro['mensagem']}
                )

    mensagens.append(
        {
            'role': 'system',
            'content': 'You are a helpful assistant.',
        }
    )
    mensagens.extend(mensagens_anteriores)
    mensagens.append(
        {
            'role': 'user',
            'content': prompt,
        }
    )
    return mensagens


def num_tokens_from_messages(messages, model='gpt-3.5-turbo-0613'):
    """
    Return the number of tokens used by a list of messages.
    https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

    TODO:
    """
    logger.info('O modelo escolhido foi %s', model)
    try:
        encoding = tiktoken.encoding_for_model(model_name=model)

    except KeyError:
        logger.error(
            'Modelo "%s" não encontrado. Usando o modelo cl100k_base encoding.',
            model,
        )
        encoding = tiktoken.get_encoding(encoding_name='cl100k_base')
    logger.info('O encoding definido é %s', encoding)

    if model in {
        'gpt-3.5-turbo-0613',
        'gpt-3.5-turbo-16k-0613',
        'gpt-4-0314',
        'gpt-4-32k-0314',
        'gpt-4-0613',
        'gpt-4-32k-0613',
    }:
        tokens_per_message = 3
        tokens_per_name = 1

    elif model == 'gpt-3.5-turbo-0301':
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4

        # if there's a name, the role is omitted
        tokens_per_name = -1

    elif 'gpt-3.5-turbo' in model:
        logger.warning(
            'Warning: gpt-3.5-turbo may update over time. '
            'Returning num tokens assuming gpt-3.5-turbo-0613.'
        )
        return num_tokens_from_messages(messages, model='gpt-3.5-turbo-0613')

    elif 'gpt-4' in model:
        logger.warning(
            'Warning: gpt-4 may update over time. '
            'Returning num tokens assuming gpt-4-0613.'
        )
        return num_tokens_from_messages(messages, model='gpt-4-0613')

    else:
        logger.critical('Deu ruim!')
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}.
            See https://github.com/openai/openai-python/blob/main/chatml.md for
            information on how messages are converted to tokens."""
        )

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == 'name':
                num_tokens += tokens_per_name

    # every reply is primed with <|start|>assistant<|message|>
    num_tokens += 3
    return num_tokens
