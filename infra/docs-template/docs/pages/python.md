# _Python_

O ANIA-TCE utilizava, originalmente, o _python_ 3.10.12 e ambiente virtual _venv_, com as dependências listadas em um arquivo `requirements.txt`.

Optou-se por converter o gerenciamento de pacotes para o [_uv_](https://docs.astral.sh/uv/): mais rápido e moderno.

???+ note "Informação"

    Caso você não tenha o [_uv_](https://docs.astral.sh/uv/), será necessário instalá-lo no seu ambiente. Para mais informações sobre como fazer isso, basta ir em [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).<br>
    ***Obs*** O *firewall* do CTIC estava bloqueando o acesso. Foi necessário solicitar liberação.

<br>

Criou-se o ambiente e se definiu a versão _python_. Alguns comandos básicos para manejar o ambiente _python_:

```shell
# Cria virtual environment
uv venv --python 3.11.12

# Ativa virtual environment (linux)
source .venv/bin/activate

# Instala todas as dependências do pyproject.toml
uv sync
uv sync --group docs
uv sync --group docs --group dev

# Desativa
deactivate
```

<br>

???+ warning "Alerta"

    Na rede do MPSP, a instalação de pacotes pelo *uv*  pode dar erros devido aos certificados autoassinados que a instituição usa, ocasionando o erro abaixo:
    ```shell
    ├─▶ client error (Connect)<br>
    ╰─▶ invalid peer certificate: UnknownIssuer
    ```

    Para contornar, adicionamos um parâmetro (ver [aqui](https://github.com/astral-sh/uv/issues/1819#issuecomment-2746736655)), criando o ambiente com o comando abaixo:
    ```shell
    uv venv --python 3.11.12 --allow-insecure-host https://github.com
    ```
