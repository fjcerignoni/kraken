# Blueprint de Modernizacao do Kraken

## 1) Diagnostico franco (sem romantizar)

O bot nao morreu por causa de linguagem. Ele perdeu tracao por combinacao de produto, UX e operacao.

Evidencias no projeto atual:
- Base fortemente acoplada em comandos prefixados com $, enquanto o ecossistema Discord migrou para slash commands e interacoes guiadas.
: [README.md](README.md), [bot/main.py](bot/main.py)
- Fluxos importantes dependem de conversa sequencial via wait_for, o que aumenta abandono, erros e race conditions.
: [bot/cogs/admin.py](bot/cogs/admin.py), [bot/cogs/raids.py](bot/cogs/raids.py)
- Integracoes HTTP sem retries, sem timeout padrao robusto e sem observabilidade.
: [bot/helpers.py](bot/helpers.py)
- Persistencia em SQLite local + JSON por servidor, bom para inicio, fraco para escalar multi-guild com confiabilidade.
: [bot/db/kraken_schema.sql](bot/db/kraken_schema.sql), [bot/helpers.py](bot/helpers.py)
- Ausencia de telemetria de produto: sem funil de onboarding, sem metrica de uso por comando, sem erro por feature.

Resumo duro: o projeto ainda tem valor de dominio (Albion + organizacao de raid), mas precisa de reposicionamento tecnico e de experiencia para voltar a ser relevante.

## 2) O que bots que deram certo fizeram (padroes de sucesso)

Padroes observados em bots de alto uso (moderacao, utilidade e game communities):
- Slash-first: descoberta melhor, menor curva de aprendizagem, autocomplete e validacao nativa.
- Flows curtos com componentes: botoes, selects e modais no lugar de perguntas longas no chat.
- Confiabilidade de servico: retries, circuit breaker, cache e filas para tarefas lentas.
- Operacao com dados: eventos de uso, dashboard de saude e backlog guiado por metricas reais.
- Distribuicao: onboarding em 60 segundos, comandos de valor imediato e mensagens com CTA claro.

## 3) Norte estrategico para a era de ouro

Meta de produto em 90 dias:
- Transformar o Kraken em "assistente operacional da guild" em vez de "colecao de comandos".

Jobs to be done principais:
- Lideranca de raid precisa montar comp em menos de 2 minutos.
- Jogador precisa decidir compra/venda de item em segundos.
- Oficiais precisam monitorar atividade sem abrir 5 ferramentas externas.

## 4) Arquitetura alvo (duas rotas)

### Rota A: Evoluir em Python (menor risco, mais rapido)

Quando escolher:
- Quer ganhar tracao em 4 a 8 semanas.
- Time ja domina Python.

Stack proposta:
- Python 3.12
- discord.py 2.x com app commands (slash)
- FastAPI para health/metrics/admin API
- PostgreSQL + SQLAlchemy 2.x + Alembic
- Redis para cache e locks
- APScheduler ou Celery para jobs
- OpenTelemetry + Prometheus + Grafana
- Sentry para erros de runtime

Beneficios:
- Reuso alto da logica atual.
- Menor custo de migracao.
- Time-to-value melhor.

### Rota B: Migrar para TypeScript (mais potencial de ecossistema)

Quando escolher:
- Quer padronizar stack JS no restante do time/produtos.
- Quer maior oferta de libs e devs para Discord no medio prazo.

Stack proposta:
- Node 22 + TypeScript
- discord.js v14
- Prisma + PostgreSQL
- BullMQ + Redis para filas
- Fastify para API interna
- OpenTelemetry + Sentry

Beneficios:
- Ecossistema Discord enorme em TS.
- Tipagem e DX muito fortes para equipe web.

Risco principal:
- Reescrita completa de regras de negocio pode atrasar ganhos de produto se feita cedo demais.

## 5) Recomendacao objetiva

Nao faco migracao de stack agora.

Plano recomendado:
1. Fase 1 e Fase 2 em Python para recuperar valor rapido.
2. Em 45 dias, decidir se continua Python ou vai para TS com base em metricas e capacidade do time.
3. Se migrar para TS, usar strangler pattern: novos modulos em TS, legado Python desligado gradualmente.

## 6) Roadmap pratico (0-90 dias)

### Fase 0 (Semana 1): Fundacao minima

- Padronizar configuracao por ambiente e secrets.
- Adicionar logging estruturado e correlation id.
- Implementar healthcheck e readiness.
- Criar eventos minimos de produto:
  - command_invoked
  - command_succeeded
  - command_failed
  - onboarding_completed

Entregavel:
- Baseline de estabilidade e visibilidade operacional.

### Fase 1 (Semanas 2-4): UX que traz usuarios de volta

- Migrar comandos core para slash:
  - /price
  - /organize_raid
  - /profile
- Trocar fluxos de confirmacao por botoes/modais.
- Criar onboarding guiado com /setup.
- Melhorar mensagens com templates mais curtos e claros.

Entregavel:
- Queda de friccao de uso e aumento de ativacao.

### Fase 2 (Semanas 5-8): Confiabilidade e escala

- Migrar SQLite para PostgreSQL.
- Introduzir Redis para cache de market e lock de jobs.
- Implementar retries com backoff nas APIs externas.
- Idempotencia para eventos de reacao e updates de raid.

Entregavel:
- Menos falha intermitente e comportamento previsivel.

### Fase 3 (Semanas 9-12): Crescimento e retencao

- Sistema de eventos da guild:
  - lembrete de raid
  - resumo semanal
  - ranking de participacao
- Feature flags para testar novidades por servidor.
- Painel de admin simples (web) para templates e permissoes.

Entregavel:
- Retencao semanal e valor percebido maiores.

## 7) Backlog de ouro (prioridade alta)

- Slash commands e autocomplete para itens/templating.
- Cache de precos com TTL e fallback.
- Anti-spam e rate limit por guild e por comando.
- Internacionalizacao PT-BR e EN-US.
- Permissao por papel do Discord (sincronizada) em vez de apenas tabela local.
- Mensagens de erro acionaveis (o que fazer agora).
- Testes automatizados de fluxo de comando critico.

## 8) Metricas que importam

Produto:
- Ativacao D1 por servidor novo.
- Usuarios ativos semanais por servidor.
- Uso semanal de comandos core.

Confiabilidade:
- Taxa de sucesso por comando.
- P95 de latencia por comando.
- Erros por 1.000 invocacoes.

Retencao:
- Servidores ativos em 7 e 30 dias.
- Reuso de organizacao de raid por semana.

## 9) Plano de migracao de dados

- Criar schema versionado com Alembic.
- Script de migracao de SQLite para PostgreSQL.
- Migrar JSON de raid_templates para tabela dedicada com versionamento.
- Rodar dual-write por janela curta e validar consistencia.

## 10) Riscos e mitigacoes

- Risco: reescrita longa sem entrega de valor.
  - Mitigacao: fases curtas com entrega semanal e metricas.
- Risco: APIs externas instaveis.
  - Mitigacao: cache + retries + fallback de dados.
- Risco: regressao de comando legado.
  - Mitigacao: camada de compatibilidade por 1 ciclo.

## 11) O que eu faria nesta ordem (acao imediata)

Semana atual:
1. Implementar observabilidade minima + telemetria de comandos.
2. Entregar /setup e /price em slash com UX nova.
3. Criar dashboard simples de saude e uso.

Proxima semana:
1. Migrar /organize_raid para interacoes e persistencia robusta.
2. Iniciar migracao para PostgreSQL sem desligar SQLite de imediato.

## 12) Criterio para decidir Python vs TypeScript em 45 dias

Escolher Python se:
- Time entrega 2 a 3 features por sprint com qualidade.
- P95 e taxa de erro ficam sob controle.

Escolher TypeScript se:
- Equipe web domina TS e o gargalo principal e velocidade de desenvolvimento de UX Discord.
- Houver necessidade clara de ecossistema JS para integracoes e contratacao.

Decisao baseada em dados, nao em hype de stack.
