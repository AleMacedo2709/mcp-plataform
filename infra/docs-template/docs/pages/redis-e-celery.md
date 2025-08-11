# Celery

O [Celery](https://docs.celeryq.dev/en/stable/) é uma biblioteca de código aberto para _python_ que facilita o processamento assíncrono de tarefas através de filas de tarefas (_task queues_). Ele permite que tarefas demoradas sejam executadas em segundo plano, fora do fluxo principal da aplicação, melhorando a escalabilidade e desempenho.

Principais Recursos do Celery:

- Processamento assíncrono: Executa tarefas de forma independente, sem bloquear o fluxo principal da aplicação.
- Alta escalabilidade: Pode distribuir tarefas entre múltiplos servidores ou _threads_.
- Flexibilidade: Integra-se facilmente com _frameworks web_ como _Django_, _Flask_ e outros.
- Resiliência: Capaz de tentar reconexões em caso de falhas e priorizar tarefas.

<br>

_Celery_ é ideal para aplicações que precisam lidar com tarefas complexas, como envio de e-mails, geração de relatórios e interação com APIs externas.

<br>

---

## _Eventlet_

O [_eventlet_](https://eventlet.readthedocs.io/en/latest/) é um pacote _python_ que fornece uma biblioteca de rede concorrente e não bloqueante. Pode ser útil na utilização do _Celery_ em _Windows_.

```shell
pip install eventlet
```

<br>

---

## _Redis_

[_Celery_](https://docs.celeryq.dev/en/stable/) e o [_Redis_](https://redis.io/) trabalham juntos. O _Redis_ é frequentemente usado como um message _broker_ para o _Celery_. O _Celery_ utiliza o _Redis_ para armazenar e gerenciar as filas de tarefas (_task queues_), permitindo que as tarefas sejam distribuídas e processadas de forma assíncrona.

Como eles funcionam juntos:

1. _Redis_ como Message Broker:

- _Celery_ envia as tarefas para o _Redis_, que atua como intermediário (_broker_).
- Os _workers_ do _Celery_ monitoram as filas no _Redis_ e processam as tarefas.

2. Fluxo básico:

- A aplicação adiciona uma tarefa à fila (armazenada no _Redis_).
- O _worker_ do _Celery_ pega a tarefa do _Redis_ e a executa.
- O resultado da tarefa pode ser armazenado no _Redis_ (ou em outro _backend_ de resultados, se configurado).

<br>

---

### No Ubuntu

Para instalar o [_Redis_](https://redis.io/pt/).

```shell
# Atualizar
sudo apt update -y && sudo apt upgrade -y

# Instalar
sudo apt install redis-server -y
```

<br>

---

### No RHEL9

Para instalar no RHEL9 li o artigo [How to install and configure redis in Red Hat Enterprise Linux](https://access.redhat.com/solutions/7006905).

```shell
# Atualizar
sudo yum update -y && sudo yum upgrade -y

# Instalar
sudo yum install redis -y
```

<br>

---

## Serviços

Para avaliar se instalou corretamente. Serve para Ubuntu e RHEL9.

```shell
# Version
redis-server --version

# Status
sudo systemctl status redis

# Enable
sudo systemctl enable redis

# Restart
sudo systemctl restart redis
```

<br>

???+ warning

    Na configuração do _Redis_, é necessário alterar a configuração _default_ para

    ```shell
    protect-mode no
    ```

    TODO: Estudar o porquê disso. Li isso na documentação do TCE e não fiz.
