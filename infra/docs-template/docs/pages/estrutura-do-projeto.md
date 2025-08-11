# Estrutura do Projeto

O _Assistente Natural de Inteligência Artificial_, mais conhecido como **ANIA**, é um sistema desenvolvido pelo _Tribunal de Contas do Estado de São Paulo_ (TCE-SP) para permitir que seus usuários tenham uma ferramenta de inteligência artificial para facilitar o trabalho. No MPSP a ferramenta passou a se chamar **Tilene**.

<br>

---

## Histórico

Em 12.12.2024 foi assinado Termo de Convênio entre TCE e MPSP

Em 27.03.2025 a _Equipe de Infra_ (CTIC) intermediou contato com TCE, para que fosse disponibilizado o código-fonte da versão ANIA-TCE com a _Equipe de Dados_ (SubInova).

Em 31.03.2025 a _Equipe de Infra_ (CTIC) compartilhou o código-fonte da [versão do ANIA instanciada no MP](https://aniauat.mpsp.mp.br/) com a _Equipe de Dados_ (SubInova).

Em 07.04.2025 o projeto passou a ser refatorado para atender as necessidades do MPSP.

Em 11.04.2025 se iniciou a "conversão" para do gerenciamento de pacotes para o [_uv_](https://docs.astral.sh/uv/): mais rápido e moderno.

Em 24.04.2025 o sistema de autenticação, utilizando as credencias do _Microsoft Entra ID_, foi concluido.

Em 08.05.2025 foi realizada reunião de apresentação do Tilene pro PGJ.

Em 12.05.2025 foi feita [RDM](http://mpecm01n01p-v/dio/RDM/_layouts/FormServer.aspx?XmlLocation=/dio/RDM/RDM/Formulario-2025-05-12T17_49_24.xml&ClientInstalled=false&Source=http%3A%2F%2Fmpecm01n01p%2Dv%2Fdio%2FRDM%2FRDM%2FForms%2FAllItems%2Easpx%3FFilterField1%3DID%26FilterValue1%3D16631%26FilterOp1%3DGeq%26OverrideScope%3DRecursiveAll%26FallbackLimit%3D16631%26ProcessQStringToCAML%3D1&DefaultItemOpen=1) para a criação do ambiente de desenvolvimento para _deploy_ do Tilene.

Em 13.05.2025 foi realizada implantação do Tilene em ambiente de desenvolvimento.

Em 15.05.2025 foi realizada implantação do Tilene em ambiente de homologação.

Entre 17.05 e 06.07 iniciaram testes da aplicação por usuários, em ambiente de homologação, onde se encontrou necessidade de ajustes.

Em 23.06.2025 passei a desenvolver uma documentação para o usuário final, bem como uma documentação técnica, utilizando [MkDocs](https://www.mkdocs.org/).

Em 25.06.2025, durante reunião com a _Equipe de Infra_, foi concedido o acesso para testes dos Modelos do [Azure AI Foundry Portal](https://ai.azure.com/). Passado também os [Preços do Serviço OpenAI do Azure](https://azure.microsoft.com/pt-br/pricing/details/cognitive-services/openai-service/?msockid=03e092c9eabc63700abd82e4eb356295).

Em 02.07.2025 divulguei uma nova versão com ajustes no ambiente de homologação.

<br>

---

## Tecnologias

O TCE cita, como resumo da abordagem utilizada, o _post_ [Question & Answering on Enterprise Knowledge Base - Azure OpenAI Service (GPT3)](https://www.linkedin.com/pulse/question-answering-enterprise-knowledge-base-azure-openai-s/). As principais tecnologias adotadas no ANIA são:

---

**_Frontend_**

- [Vue.js](https://vuejs.org/) (apenas uso básico, sem componentes)
- [Bootstrap](https://getbootstrap.com/)
- [Dropzone.js](https://www.dropzone.dev/)

<br>

---

**_Backend_**

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/), _framework web_
- [Celery](https://docs.celeryq.dev/en/stable/)/[Redis](https://redis.io/), para processamento em _background_
- Utilização de bibliotecas como [LangChain](https://www.langchain.com/), [OpenAI](https://openai.com/), [PyPDF2](https://pypdf2.readthedocs.io/en/3.x/), [tiktoken](https://github.com/openai/tiktoken), [SqlAlchemy](https://www.sqlalchemy.org/)
