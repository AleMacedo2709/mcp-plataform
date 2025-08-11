"""
No Módulo main_app.py e módulo app_noauth.py
tem muitas funções escritas que são idênticas.

Refatorei para parar com essa duplicidade.
"""

import logging

from flask import Blueprint, session, Response
from flask import render_template
from flask import send_from_directory

from ania.auth.entra import auth
from ania.indice_ania.indice_sql import IndiceSQL
from ania.paths import project_path

# from flask import session, redirect, url_for

logger = logging.getLogger(__name__)

root_bp = Blueprint('root', __name__, template_folder='templates')


@root_bp.route('/')
@auth.login_required
def index(*, context: dict):
    """
    The main page of the web app.
    :param context:
    :return:
    """
    # Necessário obter o username, pois isso permite renderizar parte do index.html
    id_usuario = context['user']['oid']
    username = context['user']['preferred_username']

    # Define a sessão como permanente, o que significa que ela não será encerrada
    # automaticamente quando o navegador for fechado.
    # Em vez disso, a sessão será armazenada por um período configurado no
    # atributo PERMANENT_SESSION_LIFETIME da aplicação Flask.
    session.permanent = True

    # Define variáveis para a session
    session['id_usuario'] = id_usuario
    session['username'] = username

    # indice = acessorios.obter_indice(categoria='usuario')
    logger.debug(f'Abaixo entro na função do índice')
    indice = IndiceSQL()
    logger.debug(f'Sai da função do índice')
    usuario = indice.login_usuario(id_usuario=id_usuario)
    print(f'O usuário logado é {usuario}')

    return render_template(template_name_or_list='index.html')


# @root_bp.route('/favicon.ico')
# def favicon() -> Response:
#     """
#     Carrega a imagem do favicon
#     """
#     return send_from_directory(
#         directory=project_path / 'static' / 'images',
#         path='favicon.ico',
#         # mimetype='image/vnd.microsoft.icon'
#         mimetype='image/x-icon',
#     )


# @root_bp.route('/favicon-96x96.png')
# def favicon96() -> Response:
#     """
#     Carrega a imagem do favicon
#     """
#     return send_from_directory(
#         directory=project_path / 'static' / 'images',
#         path='favicon-96x96.png',
#         mimetype='image/png',
#     )


# @root_bp.route('/', defaults={'path': ''})
# @root_bp.route('/<path:path>')
# def catch_all(path):
#     """
#
#     """
#     if 'email' in session:
#         return render_template('index.html')
#     return redirect(url_for('auth.login'))
