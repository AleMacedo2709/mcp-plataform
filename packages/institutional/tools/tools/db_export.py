"""
Módulo para exportar as definições do banco de dados criando um script em formato .sql.
Ele deve ser executado quando o model for modificado, para criar as DML (Data Manipulation Language) necessárias para criar as tabelas no banco de dados.
Isso se faz necessário pois em ambiente de produção não é possível executar o módulo db_create.py,
visto que o servidor de aplicação não tem permissão de DML no servidor do banco de dados.
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Literal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable, SetColumnComment, SetTableComment

from ania.indice_ania import model

# from ania.logs import model_log


class ConvertToSQL:
    """
    Converte o model para um arquivo .sql
    """

    def __init__(
        self,
        db_definition: SQLAlchemy,
        bind_key=None,
        filepath: Path = Path('.'),
    ):
        self.db_definition = db_definition
        self.filepath = filepath
        self.bind_key = bind_key

        # Deleta arquivo .sql se já existir
        self.filepath.unlink(missing_ok=True)

    def add_header(self, *args, **kwargs):
        """
        Adiciona o cabeçalho no arquivo .sql

        :param args: Lista de strings a serem adicionadas ao cabeçalho
        :param kwargs: Pares chave-valor a serem adicionados ao cabeçalho
        """

        with open(file=self.filepath, mode='a') as f:
            # Header
            f.write(f'/*{"-" * 60}\n')

            for arg in args:
                f.write(f'{arg}\n')

            f.write(f'*/{"-" * 60}\n\n')

    def add_sql(self, *args, **kwargs):
        """
        Adiciona definições no arquivo .sql

        :param args: Lista de strings a serem adicionadas ao cabeçalho
        :param kwargs: Pares chave-valor a serem adicionados ao cabeçalho
        """

        with open(file=self.filepath, mode='a') as f:
            # Extensão do PostgresSQL
            for arg in args:
                f.write(f'{arg}\n')

    def convert(self):
        """
        Converte o model para um arquivo .sql
        """
        list_tables = []
        for cls in model.db.Model.registry.mappers:
            mapped_cls = cls.class_
            #
            if self.bind_key == 'db_log':
                if (
                    hasattr(mapped_cls, '__bind_key__')
                    and getattr(mapped_cls, '__bind_key__', None) == 'db_log'
                ):
                    list_tables.append(mapped_cls.__table__)
                    # print('Entrei em db_logs')

            # Se não tem __bind_key__ e é do db_app
            elif not hasattr(mapped_cls, '__bind_key__'):
                list_tables.append(mapped_cls.__table__)
                # print('Entrei em db_apps')

        # Cria o arquivo .sql
        with open(file=self.filepath, mode='a') as f:
            for table in list_tables:
                #  Print
                print(f'Criando tabela {table.name}')

                # Definição da Tabela
                table_create = CreateTable(element=table, if_not_exists=True)

                # Compila para o PostgresSQL
                table_compile = table_create.compile(
                    dialect=postgresql.dialect(),
                )

                # Ajusta o texto
                table_compile = str(table_compile).strip()

                # Escreve no arquivo
                f.write(f'-- Cria tabela {table.name}\n')
                f.write(f'{table_compile};\n\n')

                f.write(f'-- Define comentários para a {table.name}\n')
                table_comment = SetTableComment(table)
                f.write(f'{table_comment};\n\n')

                for column in table.columns:
                    if column.comment is not None:
                        column_comment = SetColumnComment(element=column)
                        f.write(f'{column_comment};\n\n')

                f.write('\n\n')


def main(filepath: Path, schema: Literal['db_app', 'db_log']):
    """
    Função principal para gerar o arquivo .sql
    """
    print(f'Arquivo {filepath}')
    try:
        # Instancia o Conversor
        sql = ConvertToSQL(
            db_definition=model.db,
            filepath=filepath,
            bind_key=schema,
        )

        if schema == 'db_app':
            sql.add_header(
                'Script para criação das tabelas do ANIA',
                'Script criado com auxílio do módulo db_export.py\n',
                'Michel Metran',
                f'Data: {datetime.today().strftime("%d.%m.%Y")}',
            )
            sql.add_sql(
                '-- Extensão do PostgreSQL',
                'CREATE EXTENSION IF NOT EXISTS "vector";\n\n',
            )
            sql.convert()
            print('Definições do banco de dados criado com sucesso.')

        elif schema == 'db_log':
            sql.add_header(
                'Script para criação da tabela de log do ANIA',
                'Script criado com auxílio do módulo db_export.py\n',
                'Michel Metran',
                f'Data: {datetime.today().strftime("%d.%m.%Y")}',
            )
            sql.add_sql(
                '-- Extensão do PostgreSQL',
                '-- Por algum bug, é necessário criar a extensão "vector" mesmo que logs não utilize',
                'CREATE EXTENSION IF NOT EXISTS "vector";\n\n',
            )
            sql.convert()
            print('Definições do banco de dados criado com sucesso.')

    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')


if __name__ == '__main__':
    # Configura o argparse
    parser = argparse.ArgumentParser(
        description='Exporta as definições do banco de dados para um arquivo .sql.'
    )

    # Adiciona o argumento para o caminho do arquivo .sql
    parser.add_argument(
        '--filepath',
        type=str,
        default=str(
            Path(__file__).parents[0].absolute() / 'data' / 'sql' / 'schema.sql'
        ),
        help='Caminho para o arquivo .sql onde as definições serão salvas.',
    )
    # Adiciona o argumento para o schema
    parser.add_argument(
        '--schema',
        type=str,
        choices=['db_app', 'db_log'],
        default='db_app',
        help='Define o schema a ser exportado (db_app ou db_log).',
    )

    # Lê os argumentos da linha de comando
    args_app = parser.parse_args()

    # Executa a função principal com o argumento fornecido
    main(filepath=Path(args_app.filepath), schema=args_app.schema)
