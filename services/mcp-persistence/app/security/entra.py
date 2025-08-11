"""
Módulo contendo Auth do Identity
https://identity-library.readthedocs.io/en/latest/flask.html

Necessário para autenticação da Microsoft
"""

from identity.flask import Auth

from ania import config

auth = Auth(
    app=None,
    authority=f'https://login.microsoftonline.com/{config.Config.AZURE_TENANT_ID}',
    client_id=config.Config.AUTH_CLIENT_ID,
    client_credential=config.Config.AUTH_CLIENT_SECRET,
    redirect_uri=config.Config.AUTH_REDIRECT_URI
)

if __name__ == '__main__':
    print(config.Config.AZURE_TENANT_ID)
    print(auth._authority)
