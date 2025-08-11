"""
No Módulo main_app.py e módulo app_noauth.py
tem muitas funções escritas e que são idênticas...

Refatorei para parar com essa duplicidade...
"""

import logging
import time
from pathlib import Path

from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.utils import secure_filename

from ania import config, paths
from ania.auth.entra import auth

from . import tasks

# from ania.decorators.authentication import authorize


logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__, template_folder='templates')


# @authorize
@upload_bp.route('/upload', methods=['POST'])
@auth.login_required
def upload_file(
    *,
    context,
    # id_usuario, email
):
    """
    Função que está vinculada ao front-end, em uma área de drag and drop
    """
    arquivos = []
    # print('---' * 40)
    # print(context)
    # print('---' * 40)

    id_usuario = context['user']['oid']
    # username = context['user']['preferred_username']

    for item in request.files:
        # Obtém o arquivo
        uploaded_file = request.files.get(item)

        # Transforma em uma "versão" segura com werkzeug
        uploaded_file.filename = secure_filename(
            filename=uploaded_file.filename
        )
        logger.info(
            f'O arquivo que teve upload realizado é: %s', uploaded_file.filename
        )

        # Se o arquivo realmente existe
        if uploaded_file.filename != '':
            # Obtém a extensão do arquivo
            # extension = os.path.splitext(uploaded_file.filename)[1]
            extension = Path(uploaded_file.filename).suffix.lower()

            # Avalia se a extensão está disponível na aplicação
            if extension not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)

        # Obtem o tamanho do arquivo
        # print('-' * 100)
        # print(uploaded_file.content_length)
        # print(uploaded_file.content_type)

        # Salva a posição atual
        pos = uploaded_file.stream.tell()
        # Move para o final do arquivo
        uploaded_file.stream.seek(0, 2)
        size = uploaded_file.stream.tell()
        # Retorna para a posição original
        uploaded_file.stream.seek(pos)
        print(size, type(size))

        #
        max_size = current_app.config['MAX_CONTENT_LENGTH']
        if size > max_size:
            # abort(400, description="Arquivo excede o tamanho máximo permitido.")
            pass
        # print(config.MAX_CONTENT_LENGTH, type(config.MAX_CONTENT_LENGTH))
        # if int(size) > int(config.MAX_CONTENT_LENGTH):
        #     print('-' * 100)
        #     print('-ddddd')
        #     abort(400)

        # Cria diretório para o usuário
        # Corrigir o caminho usando os.path.abspath e os.path.join
        # TODO na versão do main_app.py era usado o código abaixo.

        # FIXME: Chumbei em 22.04.2025 apenas para dar certo
        # id_usuario = 1
        # email = 'michelmetran@teste.com.br'
        # diretorioArquivosUsuario = '../arquivos/' + str(idUsuario)

        # Garantir que o diretório existe
        user_path = paths.data_users_path / str(id_usuario)
        user_path.mkdir(parents=True, exist_ok=True)

        # Criar o caminho completo do arquivo
        uploaded_file_renamed = (
            user_path
            / f'{time.time()}_{Path(uploaded_file.filename).stem}{extension}'
        )
        uploaded_file_renamed_posix = uploaded_file_renamed.as_posix()

        # Salva Arquivo
        uploaded_file.save(dst=uploaded_file_renamed_posix)

        # Enviando arquivo para processamento
        try:
            logger.info(
                f'Enviando arquivo para processamento: %s',
                uploaded_file_renamed_posix,
            )

            # FIXME: Aqui tá dando erro!
            task = tasks.task_upload_file.delay(
                id_usuario=id_usuario,
                arquivo_pdf_docx=uploaded_file_renamed_posix,
            )

            # Apensa à lista
            arquivos.append(
                {'nomeArquivo': uploaded_file.filename, 'task_id': task.id}
            )

        except Exception as e:
            logger.error(f'Erro ao criar task: %s', e)
            uploaded_file_renamed.unlink()
            return 'Serviço indisponível', 500

    return jsonify(arquivos)
