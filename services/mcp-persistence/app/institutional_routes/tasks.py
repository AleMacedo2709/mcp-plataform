"""
Módulo com as tasks
"""

import logging
import os
import uuid
from pathlib import Path

from celery import shared_task
from flask import Blueprint
from flask import current_app
from flask import jsonify

from ania.indice_ania.indice_sql import IndiceSQL
from ania.outros_modulos import indexar_arquivos
from ania.outros_modulos.util import open_file

logger = logging.getLogger(__name__)

celery_bp = Blueprint('celery', __name__, template_folder='templates')


@celery_bp.route('/status/<task_id>')
def task_status(task_id):
    """
    Situação do processamento de uma tarefa
    """
    logger.warning('task_id: %s', task_id)
    #
    task = task_upload_file.AsyncResult(task_id)
    logger.debug('task: %s', task)

    if task.state == 'PENDING':
        logger.info('Entrei no PENDING')
        response = {'state': task.state, 'status': 'Pendente...'}

    elif task.state != 'FAILURE':
        logger.info('Entrei no diferente de FAILURE. O status é %s', task.state)
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'atual' in task.info:
            response['atual'] = task.info['atual']

        if 'total' in task.info:
            response['total'] = task.info['total']

        if 'nomeArquivo' in task.info:
            response['nomeArquivo'] = task.info['nomeArquivo']

        if 'result' in task.info:
            response['result'] = task.info['result']

    else:
        logger.info('Entrei em qualquer outro status: %s', task.state)
        response = {'state': task.state, 'status': str(task.info)}

    return jsonify(response)


# ---------------------------------------------------------
# FUNÇÕES COMPLEMENTARES DO CELERY


# @app_celery.task(bind=True, name='upload_file')
@shared_task(bind=True, name='upload_file')
def task_upload_file(self, id_usuario: uuid.uuid4, arquivo_pdf_docx):
    """
    Processamento de arquivos PDF

    https://stackoverflow.com/questions/37948357/flask-with-celery-application-context-not-available

    TODO: Por que tem um parâmetro self foram de uma classe?
    FIXME: Aqui tá dando erro!
    :param self:
    :param id_usuario:
    :param arquivo_pdf_docx:
    :return:
    """
    logger.info('Uploading PDF')
    logger.info(f'Celery - Iniciando processamento para usuário %s', id_usuario)
    logger.info('Celery - Arquivo: %s', arquivo_pdf_docx)

    try:
        arquivo_txt = f'{arquivo_pdf_docx}.txt'

        # Obtém o nome do arquivo após o primeiro "_".
        # arquivo = os.path.basename(arquivo_pdf_docx).split('_', 1)[-1]
        arquivo = Path(arquivo_pdf_docx).name.split(sep='_', maxsplit=1)[-1]

        logger.warning('Entender o que é isso: %s', arquivo)

        self.update_state(
            state='PROGRESS',
            meta={
                'nomeArquivo': arquivo,
                'status': 'Extraindo o texto do arquivo...',
            },
        )

        logger.info('Celery - Convertendo PDF para TXT: %s', arquivo_txt)
        indexar_arquivos.converter_arquivo_pdf_para_txt(
            caminho_do_arquivo=arquivo_pdf_docx,
            caminho_do_arquivo_txt=arquivo_txt,
        )

        logger.info('Celery - Conversão concluída')
        conteudo_arquivo = open_file(filepath=arquivo_txt)
        logger.info(
            f'Celery - Arquivo TXT lido, tamanho: %s', len(conteudo_arquivo)
        )

        # Remove os arquivos
        os.remove(arquivo_pdf_docx)
        os.remove(arquivo_txt)
        logger.info('Celery - Arquivos temporários removidos')

        tamanho = len(conteudo_arquivo)
        if tamanho == 0:
            raise Exception(
                f'Não foi possível extrair o texto do arquivo {arquivo}'
            )

        if tamanho > 3000000:
            raise Exception(
                'A quantidade de texto é superior ao limite permitido '
                '(3.000.000 caracteres).'
            )

        logger.info('Celery - Obtendo dados do arquivo...')
        dados_dos_arquivos = indexar_arquivos.obter_dados_arquivo(
            arquivo=arquivo, conteudo_arquivo=conteudo_arquivo, celery_task=self
        )

        try:
            self.update_state(
                state='PROGRESS',
                meta={
                    'nomeArquivo': arquivo,
                    'status': 'Armazenando os dados...',
                },
            )
        except Exception as e:
            logger.error('Algum erro\n%s', e)
            raise e

        logger.info('Celery - Iniciando contexto do app...')
        try:
            with current_app.app_context():
                # indice = acessorios.obter_indice(categoria='usuario')
                indice = IndiceSQL()
                logger.info('Celery - Adicionando ao índice...')
                indice.adicionar(
                    id_usuario=id_usuario, novos_registros=dados_dos_arquivos
                )
                logger.info('Celery - Índice atualizado')

        except Exception as e:
            logger.error('Algum erro\n%s', e)
            raise e

        return {
            'id_usuario': id_usuario,
            'nomeArquivo': arquivo,
            'status': 'Arquivo processado com sucesso.',
            'result': 'OK',
        }

    except Exception as e:
        # logger.info(f'Celery - Erro no processamento %s', e, exc_info=True)
        logger.exception(
            'Erro no processamento do arquivo %s', arquivo_pdf_docx
        )
        raise e
