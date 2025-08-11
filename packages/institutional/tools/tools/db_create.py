"""
Módulo para criar as tabelas do banco de dados
Esse módulo é responsável por criar as tabelas necessárias para a aplicação.
Ele deve ser executado apenas uma vez, quando a aplicação for instalada.
Ele não deve ser executado em produção, apenas em desenvolvimento.
"""

import argparse
from typing import Literal

from ania import create_app
from ania.indice_ania import model
from ania.logs import model_log


def main(schema: Literal['db_app', 'db_log'], drop: bool = True):
    """
    Função principal do módulo

    :return: None
    """

    try:
        app = create_app()
        with app.app_context():

            if schema == 'db_app':
                if drop is True:
                    print(f'Deletando o banco de dados "{schema}"')
                    model.db.drop_all()

                print(f'Criando o banco de dados "{schema}"')
                model.db.create_all()

            elif schema == 'db_log':
                if drop is True:
                    print(f'Deletando o banco de dados "{schema}"')
                    model_log.db.drop_all()

                print(f'Criando o banco de dados "{schema}"')
                model_log.db.create_all()

        print('Banco de dados criado com sucesso.')

    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')


if __name__ == '__main__':
    # Configura o argparse
    parser = argparse.ArgumentParser(description='Cria o banco de dados')

    # Adiciona o argumento para deletar o banco de dados
    parser.add_argument(
        '-d',
        '--drop',
        action='store_true',
        help='Deleta o banco de dados antes de criar',
    )
    # Adiciona o argumento para o schema
    parser.add_argument(
        '--schema',
        type=str,
        choices=['db_app', 'db_log'],
        default='db_app',
        help='Define o schema a ser criado (db_app ou db_log).',
    )

    # Lê os argumentos da linha de comando
    args_app = parser.parse_args()

    # Executa a função principal com o argumento fornecido
    main(drop=args_app.drop, schema=args_app.schema)
