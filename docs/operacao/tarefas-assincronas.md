# Tarefas Assíncronas — Melhor Prática

**Opção A (recomendada):** mover a lógica de análise para o **worker Celery**, importando o pacote de ingestão (biblioteca compartilhada).
- Reduz latência e dependência de chamadas HTTP internas.
- Torna a tarefa idempotente e autocontida.
- Facilita **retry** e **observabilidade** de ponta a ponta.

**Opção B:** chamar um endpoint interno síncrono do serviço de ingestão a partir do worker.
- Adiciona dependência de rede e pontos de falha extras.
- Útil apenas quando há **restrições fortes** de isolamento de código.

> Vamos manter o caminho de migração para **A**, extraindo o `LLMAnalyzer` e normalizador para um **módulo compartilhado** e usando-o diretamente dentro do worker.
