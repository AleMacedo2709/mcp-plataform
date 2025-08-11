"""
No Módulo main_app.py e módulo app_noauth.py
tem muitas funções escritas e que são idênticas...

Refatorei para parar com essa duplicidade...
"""

import json
import logging
import time
import uuid

from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    request,
    session,
    stream_with_context,
)

from ania import paths
from ania.auth.entra import auth
from ania.ia import api_openai
from ania.indice_ania.indice_sql import IndiceSQL
from ania.outros_modulos.util import open_file

# from ania.decorators.authentication import authorize

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, template_folder='templates')


# @authorize
@api_bp.route('/lista_arquivos_exemplo', methods=['GET'])
@auth.login_required
def lista_arquivos(*, context: dict) -> Response:
    """
    TODO: Descrever o que faz
    """
    logger.info('Lista arquivos exemplo')

    # Obtem Índice
    indice = IndiceSQL()
    # indice = acessorios.obter_indice(categoria='exemplos')
    arquivos = indice.obter_lista_arquivos(id_usuario=None)

    #
    retorno = []
    for arquivo in arquivos:
        retorno.append({'nomeArquivo': arquivo})

    return jsonify(retorno)


# @authorize
@api_bp.route('/lista_arquivos_usuario', methods=['GET'])
@auth.login_required
def lista_arquivos_usuario(*, context: dict) -> Response:
    """
    Descrever o que a função

    :param context:
    :return:
    """
    logger.info('Lista arquivos usuario')

    # FIXME: Coloquei em 22.04.2025 APENAS PARA CONTORNAR O GARGALO DA NOVA AUTENTICAÇÃO
    id_usuario = context['user']['oid']
    # username = context['user']['preferred_username']
    # session['username'] = username

    # print('*' * 60)
    # print(user)
    # print(context)
    # print('*' * 60)

    if id_usuario is not None:
        # indice = acessorios.obter_indice(categoria='usuario')
        indice = IndiceSQL()
        arquivos = indice.obter_lista_arquivos(id_usuario=id_usuario)

    else:
        arquivos = []
        logger.critical(
            'Como entrei aqui!? É possível não ter usuário na aplicação?!'
        )

    retorno = []
    for arquivo in arquivos:
        retorno.append({'nomeArquivo': arquivo})

    return jsonify(retorno)


# @authorize
@api_bp.route('/pesquisar', methods=['POST'])
@auth.login_required
def pesquisar(*, context: dict):
    """
    Pesquisa
    Usado no Tilene.GPT, sem contexto de documentos!

    :param context:
    :return:
    """
    id_usuario = context['user']['oid']
    # username = context['user']['preferred_username']
    # session['username'] = username

    logger.info('Pesquisa documentos')

    # Get Data
    json_data = request.get_json()
    pergunta = json_data['pergunta']
    historico = json_data['historico']
    categoria = json_data['categoria']
    modelo_gpt = json_data['modeloGPT']
    logger.info('Pesquisar com parâmetros %s', json_data)

    if not categoria or not pergunta or not modelo_gpt:
        return 'Parâmetros não informados', 400

    # Instancia Índice
    # indice = acessorios.obter_indice(categoria=categoria)
    indice = IndiceSQL()

    # FIXME: Chumbei em 22.04.2025, apenas para testes
    # id_usuario = 1
    # id_usuario = id_usuario if categoria == 'usuario' else None
    if categoria != 'usuario':
        id_usuario = None

    try:
        if categoria == 'ChatGPT':
            embedding_total_tokens = None
            prompt_ajustado = pergunta
            referencias = []
            nome_arquivo = 'ChatGPT'

        else:
            nome_arquivo = None
            embedding_da_pergunta, embedding_total_tokens = (
                api_openai.criar_embedding(texto=pergunta)
            )

            # if (modelo_gpt == 'gpt-3.5-turbo-16k') or (modelo_gpt == 'gpt-4o'):

            if modelo_gpt in {'gpt-3.5-turbo-16k', 'gpt-4o'}:
                arquivo_prompt = paths.data_prompts_path / 'prompt_16k.txt'
                referencias = indice.pesquisar(
                    id_usuario=id_usuario,
                    embedding_da_pergunta=embedding_da_pergunta,
                    limite=12,
                )

            else:
                arquivo_prompt = paths.data_prompts_path / 'prompt.txt'
                # id_usuario = id_usuario if categoria == 'usuario' else None
                referencias = indice.pesquisar(
                    id_usuario=id_usuario,
                    embedding_da_pergunta=embedding_da_pergunta,
                    limite=3,
                )

            if not arquivo_prompt.is_file():
                raise Exception('Não existe o arquivo de prompt!')

            texto_referencias = ''
            for referencia in referencias:
                texto_referencias += referencia['texto'] + '\n\n'

            logger.debug('Referências obtidas. Enviando prompt...')

            prompt_ajustado = (
                open_file(filepath=arquivo_prompt)
                .replace('<<REFERENCIAS>>', texto_referencias)
                .replace('<<PROMPT>>', pergunta)
            )

        response, num_tokens_prompt = api_openai.completion(
            prompt_ajustado, historico, modelo_gpt
        )

        # # TODO: Retirar daqui....
        # log_arquivo = (
        #     'LOG_ARQUIVOS' in current_app.config
        #     and current_app.config['LOG_ARQUIVOS'] == True
        # )
        # logger.info('O valor de "log_arquivo" é "%s"', log_arquivo)

        return Response(
            stream_with_context(
                stream_resposta(
                    indice,
                    id_usuario=id_usuario,
                    arquivo=nome_arquivo,
                    response=response,
                    referencias=referencias,
                    embedding_total_tokens=embedding_total_tokens,
                    num_tokens_prompt=num_tokens_prompt,
                    prompt=prompt_ajustado,
                )
            ),
            mimetype='text/event-stream',
            headers={'X-Accel-Buffering': 'no'},
        )

    except Exception as e:
        return str(e), 500


# @authorize
@api_bp.route('/pesquisar_documento', methods=['POST'])
@auth.login_required
def pesquisar_documento(
    *,
    context: dict,
    # id_usuario, email
):
    """
    Rest of the endpoints remain the same,
    just with the existing @authorize decorator


    # TODO: Ajustar
    """
    id_usuario = context['user']['oid']
    username = context['user']['preferred_username']
    session['username'] = username

    # print(context["user"])
    # print(session['email'])

    logger.info('Pesquisa documentos')

    # Get Data
    json_data = request.get_json()
    prompt = json_data['prompt']
    nome_arquivo = json_data['nomeArquivo']
    categoria = json_data['categoria']
    historico = json_data['historico']
    modelo_gpt = json_data['modeloGPT']
    logger.debug('O json é %s', json_data)
    if not categoria or not prompt or not modelo_gpt:
        return 'Parâmetros não informados', 400

    # Obtém Usuário
    # FIXME: Chumbei em 22.04.2025, apenas para testes
    if categoria != 'usuario':
        id_usuario = None
        logger.warning('A categoria é %s', categoria)

    logger.debug('O usuário é %s', id_usuario)

    #
    # indice = acessorios.obter_indice(categoria=categoria)
    indice = IndiceSQL()

    try:
        embedding_da_pergunta, embedding_total_tokens = (
            api_openai.criar_embedding(texto=prompt)
        )

        if (modelo_gpt == 'gpt-3.5-turbo-16k') or (modelo_gpt == 'gpt-4o'):
            arquivo_prompt = paths.data_prompts_path / 'prompt_16k.txt'
            # arquivo_prompt = '../prompt_16k.txt'
            # id_usuario = id_usuario if categoria == 'usuario' else None
            registros = indice.pesquisar_no_documento(
                id_usuario=id_usuario,
                arquivo=nome_arquivo,
                limite=12,
                embedding_da_pergunta=embedding_da_pergunta,
            )

        else:
            arquivo_prompt = paths.data_prompts_path / 'prompt.txt'
            # arquivo_prompt = '../prompt.txt'
            # id_usuario = id_usuario if categoria == 'usuario' else None
            registros = indice.pesquisar_no_documento(
                id_usuario=id_usuario,
                arquivo=nome_arquivo,
                limite=2,
                embedding_da_pergunta=embedding_da_pergunta,
            )

        texto_documento = ''
        for registro in registros:
            texto_documento += registro['texto'] + '\n\n'

        logger.info('Referências obtidas. Enviando prompt...')

        if not arquivo_prompt.is_file():
            logger.error(
                'Arquivo de prompt não encontrado %s (%s) (%s)',
                arquivo_prompt,
                type(arquivo_prompt),
                arquivo_prompt.is_file(),
            )
            # raise Exception('Arquivo prompt não encontrado')

        prompt_ajustado = (
            open_file(filepath=arquivo_prompt)
            .replace('<<PROMPT>>', prompt)
            .replace('<<REFERENCIAS>>', texto_documento)
        )

        response, num_tokens_prompt = api_openai.completion(
            prompt=prompt_ajustado,
            historico=historico,
            modelo_gpt=modelo_gpt,
            max_tokens=500,
        )

        # TODO: Retirar daqui....
        # log_arquivo = (
        #     'LOG_ARQUIVOS' in current_app.config
        #     and current_app.config['LOG_ARQUIVOS'] == True
        # )
        # logger.info('O valor de "log_arquivo" é "%s"', log_arquivo)

        # FIXME: Debugging middleware caught exception in streamed response at a point where response headers were already sent.
        # with current_app.app_context():
        # resposta = 1

        return Response(
            stream_with_context(
                stream_resposta(
                    indice,
                    id_usuario,
                    nome_arquivo,
                    response,
                    registros,
                    embedding_total_tokens,
                    num_tokens_prompt,
                    prompt_ajustado,
                )
            ),
            mimetype='text/event-stream',
            headers={'X-Accel-Buffering': 'no'},
        )

    except Exception as e:
        logger.error(e)
        return str(e), 500


# @authorize
@api_bp.route('/excluir_documento', methods=['POST'])
@auth.login_required
def excluir_documento(*, context: dict):
    """
    Excluir documento
    """
    logger.info('Excluir documento')

    # Pega id do Usuário
    id_usuario = context['user']['oid']

    # Get Data
    json_data = request.get_json()
    nome_arquivo = json_data['nomeArquivo']

    #
    if not nome_arquivo:
        return 'Parâmetros não informados', 400

    try:
        # indice = acessorios.obter_indice(categoria='usuario')
        indice = IndiceSQL()
        indice.excluir(id_usuario=id_usuario, arquivo=nome_arquivo)
        return jsonify(success=True)

    except Exception as e:
        logger.error(e)
        return str(e), 500


# ---------------------------------------------------------
# FUNÇÕES ACESSÓRIAS


def stream_resposta(
    indice,
    id_usuario: uuid.UUID,
    arquivo,
    response,
    referencias,
    embedding_total_tokens,
    num_tokens_prompt,
    prompt,
    log_arquivo=True,
):
    """
    A função stream_resposta é responsável por enviar respostas parciais
    (streaming) para o frontend durante o processamento de uma requisição,
    geralmente em aplicações que usam IA/chat (como OpenAI GPT).
    Ela é usada como um generator para enviar dados em
    tempo real via HTTP (com text/event-stream).

    O que ela faz, passo a passo:
    1. Recebe vários parâmetros:
    `indice`: objeto para logar uso e buscar dados.
    `id_usuario`, arquivo, referencias, etc.: informações do contexto da requisição.
    `response`: objeto iterável com as respostas geradas (ex: tokens do modelo de IA).
    `prompt`, `log_arquivo`: prompt enviado e flag para logar em arquivo.

    2. Itera sobre a resposta:
    Para cada linha/token gerado pelo modelo, extrai o texto e envia
    imediatamente para o frontend usando `yield 'data:' + json.dumps(text) + '\n\n'`.
    Isso permite que o usuário veja a resposta sendo construída em tempo real.

    3. Conta tokens e monta a resposta completa:
    Vai acumulando o texto e contando quantos tokens foram enviados.

    4. Ao final:
    Envia um evento especial `DONE` para indicar o fim da resposta.
    Envia as referências usadas na resposta.
    Faz logging do uso de tokens no banco de dados.
    Se log_arquivo for True, salva o prompt e a resposta em um arquivo de log.

    5. Contexto Flask:
    Usa `current_app.app_context()` para garantir que operações de logging
    funcionem corretamente dentro do contexto da aplicação Flask.
    """
    try:
        resposta = ''
        num_tokens_resposta = 0
        yield ''
        for line in response:
            if hasattr(line, 'choices'):
                # print('Printando Choices')
                # print(line.choices)
                # print(line)
                if len(line.choices) > 0:
                    text = line.choices[0].delta.get('content', '') or ''

                else:
                    text = line

            else:
                text = line

            if len(text):
                yield 'data:' + json.dumps(text) + '\n\n'
                resposta = resposta + text
                num_tokens_resposta += 1
        yield 'data:DONE\n\n'
        yield 'event:referencias\n'
        yield 'data:' + json.dumps(referencias)

    finally:
        # import tiktoken
        # encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
        # num_tokens = len(encoding.encode(resposta))
        completion_total_tokens = num_tokens_prompt + num_tokens_resposta
        with current_app.app_context():
            if embedding_total_tokens is not None:
                indice.log(
                    id_usuario=id_usuario,
                    arquivo=arquivo,
                    total_tokens=embedding_total_tokens,
                    api='embedding',
                )
            indice.log(
                id_usuario=id_usuario,
                arquivo=arquivo,
                total_tokens=completion_total_tokens,
                api='completion',
            )

        # Log
        if log_arquivo:
            # FIXME:
            # diretorio_log = (
            #     os.path.dirname(os.path.realpath(__file__)) + '/../openai_logs'
            # )
            # os.makedirs(diretorio_log, exist_ok=True)

            # Cria o diretório
            diretorio_log = paths.data_arquivo_logs_openai_path
            diretorio_log.mkdir(parents=True, exist_ok=True)

            arquivo_log = diretorio_log / f'{time.time()}_openai.txt'
            with open(file=arquivo_log, mode='w', encoding='utf-8') as f:
                f.write(
                    f'ID_USUARIO: {id_usuario}'
                    + '\n\nPROMPT:\n\n'
                    + prompt
                    + '\n\n**************************\n\nRESPOSTA:\n\n'
                    + resposta
                    + f'\n\nOpenAI API - total_tokens: {completion_total_tokens}'
                )


# def ania_dados_stream_resposta(response):
#     """
#     Não utilizaod pelo MPSP
#
#     :rtype: Generator[str, Any, None]
#     """
#     response = response or ''
#     resposta = ''
#     yield ''
#     for text in response:
#         if len(text):
#             yield 'data:' + json.dumps(text) + '\n\n'
#             resposta = resposta + text
#     yield 'data:DONE\n\n'


# ---------------------------------------------------------
# Funções abaixo não são usadas pelo MPSP


# # @authorize
# @api_bp.route('/ania_dados_pesquisar', methods=['POST'])
# @auth.login_required
# def ania_dados_pesquisar(
#     *,
#     context,
#     # id_usuario, email
# ):
#     """
#     Inclusão do ANIA.dados
#     MPSP não usa essa função!
#     """
#     logger.info('ANIA.Dados')
#     json_data = request.get_json()
#     pergunta = json_data['pergunta']
#     verbosidade = json_data['verbosidade']

#     if not pergunta or not verbosidade:
#         return 'Parâmetros não informados', 400

#     try:
#         api_url = current_app.config['API_ANIA_DADOS_URL']

#         verbose = verbosidade == 'textual'
#         headers = {'Content-Type': "application/json"}
#         dados_requisicao = {'pergunta': pergunta, 'verbose': verbose}

#         if 'API_ANIA_DADOS_KEY' in current_app.config:
#             headers['Ocp-Apim-Subscription-Key'] = current_app.config[
#                 'API_ANIA_DADOS_KEY'
#             ]

#         verify_ssl_certificate = True
#         if (
#             'API_ANIA_DADOS_VERIFY_SSL_CERTIFICATE' in current_app.config
#             and current_app.config['API_ANIA_DADOS_VERIFY_SSL_CERTIFICATE']
#             is False
#         ):
#             verify_ssl_certificate = False

#         response = requests.post(
#             url=api_url,
#             json=dados_requisicao,
#             headers=headers,
#             verify=verify_ssl_certificate,
#         )
#         response.raise_for_status()

#         dados_retorno = response.json()
#         resposta = dados_retorno.get('resposta')

#         return Response(
#             ania_dados_stream_resposta(response=resposta),
#             mimetype='text/event-stream',
#             headers={'X-Accel-Buffering': 'no'},
#         )

#     except Exception as e:
#         return str('ANIA.dados - %s' % e), 500


# # @authorize
# @api_bp.route('/ania_dados_saude_pesquisar', methods=['POST'])
# @auth.login_required
# def ania_dados_saude_pesquisar(*, context: dict) -> Response:
#     """
#     Inclusão do ANIA Dados Saúde
#     MPSP não usa essa função!
#     """
#     json_data = request.get_json()
#     pergunta = json_data['pergunta']
#     verbosidade = json_data['verbosidade']

#     if not pergunta or not verbosidade:
#         return 'Parâmetros não informados', 400

#     try:
#         api_url = current_app.config['API_ANIA_DADOS_SAUDE_URL']

#         verbose = verbosidade == 'textual'
#         headers = {'Content-Type': 'application/json'}
#         dados_requisicao = {'pergunta': pergunta, 'verbose': verbose}

#         if 'API_ANIA_DADOS_SAUDE_KEY' in current_app.config:
#             headers['Ocp-Apim-Subscription-Key'] = current_app.config[
#                 'API_ANIA_DADOS_SAUDE_KEY'
#             ]

#         verify_ssl_certificate = True
#         if (
#             'API_ANIA_DADOS_SAUDE_VERIFY_SSL_CERTIFICATE' in current_app.config
#             and current_app.config[
#                 'API_ANIA_DADOS_SAUDE_VERIFY_SSL_CERTIFICATE'
#             ]
#             is False
#         ):
#             verify_ssl_certificate = False

#         response = requests.post(
#             url=api_url,
#             json=dados_requisicao,
#             headers=headers,
#             verify=verify_ssl_certificate,
#         )
#         response.raise_for_status()

#         dados_retorno = response.json()
#         resposta = dados_retorno.get('resposta')

#         return Response(
#             ania_dados_stream_resposta(response=resposta),
#             mimetype='text/event-stream',
#             headers={'X-Accel-Buffering': 'no'},
#         )

#     except Exception as e:
#         return str('ANIA.dados.saude - %s' % e), 500


#
# if __name__ == '__main__':
#     aaa = os.path.dirname(os.path.realpath(__file__))
#     print(aaa)
