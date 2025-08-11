# Modificações no Projeto Original

## Variáveis de Ambiente

Eu desejava usar o _Azure Key Vault_, porém é complexo conseguir autorização para isso no MP. Optei por usar variáveis de ambiente em um arquivo `.env`. Para ler o arquivo correto, a depender de qual ambiente estou instanciando a aplicação, coloquei uma forme de ler o _hostname_ no arquivo `config.py`.

```python
import socket

hostname = socket.gethostname()
if hostname == 'mptilene01d-v.mp.sp.gov':
  ...
```

<br>

---

## APP Prefix

Observei que todas as rotas do ANIA-TCE contam com um parâmtro chamado PREFIX. Não entendi sua utilização, visto que eu acreditava que o Flask possui solução para esse tipo de situação.
Lendo o _post_ [Add a prefix to all Flask routes](https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes) entendi que há essa possibilidade simplesmente adotando uma configuração a ser definida em `app.config["APPLICATION_ROOT"] = "/abc/123"`.

Devido a isso, optei por remover a complexidade da definição manual, em cada rota, do parâmetro `PREFIX`.

<br>

---

## Caminho das pastas

Observei que a aplicação original buscava os arquivos de diversas maneiras distintas. Ora era usado o pacote `os` e diversas derivações do `os.path`, ora era usado o caminho escrito em formato _string_ diretamente e ora era usado a biblioteca `pathlib`.

Eu optei por criar um módulo chamado `path.py` e deixar os caminhos de binários (ou pastas de binários) usados na aplicação diretamente definidos e, ainda, agregar validações nas funções para avaliar se o arquivo foi, de fato, encontrado pela aplicação.

Aproveitei para padronizar as extensões em minúsculas, visto que da maneira como estava, só aceitava `.pdf` e `.docx`. Se enviassem um `.PDF` (que pode ocorrer), não aceitava.

<br>

---

## Funções

Há muitas funções do lado do cliente, escritas em _.js_.

Estudar isso...

<br>

---

## Documentação no _Sharepoint_

Na implantação do sistema no TCESP existe uma FAQ implantada no _Sharepoint_.
Caso o órgão não utilize este método, é necessário alterar uma linha do `index.html`.
Esta linha é exemplificada no código como:

```html
<a href="https://url_orgao.sharepoint.com/sites/ANIA/SitePages/Ajuda-e-Suporte.aspx" class="nav-link text-dark text-truncate" target="_blank">Ajuda e Suporte</a>
```

<br>

Ver mais detalhes em [documentação](como-instanciar.md#mkdocs_documentacao).

<br>

---

## Como alterar as informações, limitações e textos

Alterar arquivos do diretório _templates_:

- `index.html`: chat
- `pages/informacoes.html`: textos da opção "Informações", com aviso e limitações
- `pages/termo.html`: tela inicial com o termo e botão "Estou ciente e concordo"

<br>

---

## Inclusão ou alteração dos exemplos

Estes são os textos que aparecem em ANIA.legis e possuem `id_usuario = NULL` na tabela de textos.

```sql
SELECT id, id_usuario, arquivo, texto, num_tokens, embedding
FROM public.textos
WHERE id_usuario is null;
```

<br>

Para incluir um novo arquivo, siga o procedimento:

1. Use o próprio sistema e faça o _upload_ do arquivo com seu próprio usuário.
2. Selecionar os textos pelo _id_usuario_ e arquivo na tabela textos e substituir o _id_usuario_ destes registros por _NULL_.
3. Incluir o arquivo PDF em /opt/ANIA/arquivos/exemplos (no caso do teste).
4. Testar o funcionamento no sistema e verificar se o _link_ para o arquivo também funciona.

<br>

---

## Erro Barra

Notei que a barra com o botão sair, logout e o nome do email sumia às vezes. Dai, lendo o arquivo `index.html` encontrei que é necessário que na sessão tenha o _cookie_ `email`.

Resolvi mudar para `session['username']`

```html
<!-- Conteúdo Principal -->
<div class="d-flex align-items-center gap-3">
  {% if session['email'] %}
  <span class="material-symbols-rounded"> account_circle</span>
  {{ session['email'] }}
  <a href="{{ url_for('identity.logout') }}" class="d-flex align-items-center gap-2 account"> Sair </a>
  {% endif %}
</div>
```

<br>

---

## Outras Modificações

1. Faltava modularização. Todo o código estava em poucos arquivos, não separando as camadas de responsabilidade de cada módulo. Corrigido.
   - Lendo o _post_ [How to organize a relatively large Flask application?](https://stackoverflow.com/questions/9395587/how-to-organize-a-relatively-large-flask-application) tomei conhecimento do projeto [imwilsonxu/fbone](https://github.com/imwilsonxu/fbone) e vi muita recomendação de usar o _blueprint_ para fins de organização.
   - Para tomar ciência geral do que é o [ _blueprint_](https://flask.palletsprojects.com/en/stable/blueprints/), assisti o vídeo [Flask Login, Blueprints, Autenticação e Rotas Privadas](https://www.youtube.com/watch?v=m7rQBybbGQM).
2. Havia muitas funções duplicadas, bem como funções que não eram utilizadas na aplicação. Ajustado.
3. Havia importação de módulos que estavam fora da aplicação `sys.path.append("..")`. Não segue boas práticas. Ajustado.
4. Havia conflito de nome de objetos, pacotes e módulos. Corrigido.
5. Havia declaração de variáveis com palavras reservadas. Corrigido.
6. Não havia _logs_ para "debugar" a aplicação. Atualmente toda a aplicação conta com _logs_ permitindo encontrar os erros e corrigi-los.
7. Não havia documentação estruturada. Atualmente fiz um [_wiki_](https://dev.azure.com/mpsp/CGE/_wiki/wikis/ANIA_TCE_Core/) que permite que quem for técnico e for contribuir consiga seguir um roteiro para "subir" a aplicação. Isso também será útil para a equipe que irá colocar a aplicação em produção.
8. O sistema de filas e _tasks_ foi atualizado e, além do [Celery](https://docs.celeryq.dev/en/stable/), é possível monitorar as tarefas usando o [_flower_](https://flower.readthedocs.io/en/latest/).
9. O gerenciamento de dependências foi atualizado, passando do arquivo `requirements.txt` para o gerenciamento de dependência pelo [uv](https://docs.astral.sh/uv/). Também foi removido os `requirements.txt` adicionais.
