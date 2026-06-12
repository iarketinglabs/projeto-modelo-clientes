---
name: observabilidade-stack-atomica
description: Use esta skill para planejar ou implementar observabilidade em projetos Atomica. Ela cobre a stack OpenTelemetry, Prometheus, Grafana, Loki e Sentry, incluindo logging estruturado, tracing distribuido, metricas, alertas e health checks. Dispare sempre que o usuario mencionar observability, monitoring, logging, tracing, metricas, alertas, health checks, OpenTelemetry, Prometheus, Grafana, Sentry ou quando precisar instrumentar Next.js, Python, n8n ou Supabase.
---

# Observabilidade Stack Atomica

Skill para implementar a stack de observabilidade padrao dos projetos Atomica.

## Quando usar

- O usuario pede para adicionar observabilidade, monitoramento, logging, tracing, metricas, alertas ou health checks.
- Aparecem ferramentas como OpenTelemetry, Prometheus, Grafana, Loki, Sentry, Jaeger, Tempo ou Pino.
- E necessario instrumentar servicos Next.js, Python, n8n ou Supabase.
- O time vai fazer deploy de um novo servico e precisa validar visibilidade operacional.

## Responsavel no processo Atomica

Tech Lead / DevOps

## Workflow recomendado

1. **Inventarie os servicos**: Next.js, Python, n8n, Supabase, bancos, filas.
2. **Escolha o backend**: self-hosted (Prometheus + Grafana + Loki + OTel Collector) ou Grafana Cloud free tier.
3. **Instrumente cada servico**: logs JSON, traces OTel, endpoint `/metrics`.
4. **Configure o coletor OTel**: recepcao OTLP, processamento e export para Prometheus/Grafana Tempo/Loki.
5. **Crie dashboards no Grafana**: saude, latencia, erros, recursos, negocio.
6. **Defina alertas**: latencia, taxa de erro, indisponibilidade de `/health`.
7. **Valide antes do deploy**: siga `references/pre-deploy-checklist.md`.

## Visao da stack

A arquitetura padrao une quatro pilares da observabilidade com ferramentas open source e tiers gratuitos:

| Pilar | Ferramenta | Onde entra |
|---|---|---|
| Logs estruturados | Pino / python-json-logger / structlog + Loki | stdout -> Loki via driver Docker ou Fluent Bit |
| Tracing distribuido | OpenTelemetry SDK + Collector -> Grafana Tempo / Jaeger | Correlaciona requisicoes entre Next.js, Python e banco |
| Metricas | Prometheus + Grafana | Scraping de `/metrics` e dashboards |
| Erros | Sentry (free tier) | Captura excecoes e breadcrumbs em Next.js e Python |
| Alertas | Grafana Alerting ou Alertmanager | Webhooks para Slack/Discord |
| Health checks | Endpoint `/health` + Docker HEALTHCHECK | Load balancer e monitoramento de disponibilidade |

Cada servico gera telemetria em um formato padronizado. O OpenTelemetry atua como a camada comum que coleta traces, metricas e logs, enviando para os backends adequados.

## Instrumentacao por servico

### Next.js

Use `@vercel/otel` para instrumentacao nativa. Configure logs JSON com Pino. A stack Vercel ja oferece suporte a OTel, entao o esforco e minimo. Para detalhes e snippets, leia `references/nextjs-otel.md`.

### Python

Use `opentelemetry-sdk` com `TracerProvider` e `BatchSpanProcessor`. Para logs JSON, use `python-json-logger` ou `structlog`. O `LoggingInstrumentor` injeta `trace_id` e `span_id` automaticamente nos logs. Veja exemplos completos em `references/python-otel.md`.

### n8n

Habilite metricas Prometheus com a variavel de ambiente `N8N_METRICS=true`. O n8n usa `prom-client` internamente e expoe metricas de filas e processamento no endpoint padrao. Inclua o endpoint no scraping do Prometheus.

### Supabase

O Supabase ja expoe um endpoint Prometheus nativo com cerca de 200 metricas Postgres. Adicione esse endpoint ao `scrape_configs` do Prometheus e importe dashboards oficiais do Supabase no Grafana.

## Coletor OpenTelemetry

Use um coletor OTel auto-hospedado via Docker. Ele recebe telemetria dos servicos por OTLP e exporta para os backends:

- Traces -> Grafana Tempo ou Jaeger (ou diretamente ao Sentry).
- Metricas -> Prometheus.
- Logs -> Loki (via fluentd/Fluent Bit ou Docker Loki driver).

Voce pode usar a distribuicao oficial OTel Collector ou o Grafana Alloy. A vantagem de manter um coletor central e desacoplar os servicos dos backends: trocar um provedor de observabilidade nao exige alterar codigo.

## Dashboards no Grafana

Crie pelo menos um dashboard de status para Tech Leads com:

- Estado dos servicos (up/down).
- Latencia media e percentis (p50, p95, p99) de requisicoes.
- Taxa de erro (5xx, excecoes).
- CPU, memoria, disco e rede das instancias.
- Metricas de negocio (pedidos, vendas, conversoes).

Use anotacoes para marcar deploys recentes e cores de alerta (vermelho/laranja) quando metricas ultrapassarem limites. Importe templates oficiais do Supabase e Grafana para acelerar.

## Alertas

Defina regras baseadas em metricas criticas:

- Latencia media acima de 500ms por 5 minutos.
- Taxa de erro 5xx acima de 1% por 2 minutos.
- Endpoint `/health` retornando erro por mais de 1 minuto.
- Uso de CPU ou memoria acima de 80%.

Configure contact points no Grafana Alerting (Slack/Discord) e faca um teste de notificacao antes de considerar pronto. Templates de mensagem ajudam a comunicar contexto rapidamente.

## Health checks

Todo servico deve expor um endpoint `/health` que retorna 200 quando funcional e 503 quando alguma dependencia critica falha. Verifique conexoes com banco, cache ou filas quando fizer sentido.

No Docker Compose, adicione a diretiva `healthcheck` para que o proprio container sinalize saude. Exemplos de implementacao em Python, Node e configuracoes Docker estao em `references/health-check-examples.md` e `references/docker-compose-healthcheck.md`.

## Logs estruturados

Prefira JSON em todos os servicos. Logs JSON permitem consultas eficientes no Loki e correlacao automatica com traces. Padronize niveis (`info`, `warn`, `error`) e inclua metadados como `service`, `environment`, `trace_id`, `span_id` e `user_id`. Isso reduz o tempo de debug porque voce pode filtrar e saltar entre logs e traces no Grafana.

## Custos e tiers gratuitos

A stack e projetada para custo baixo:

- Prometheus, Grafana, Loki, OpenTelemetry e n8n sao open source.
- Grafana Cloud free tier cobre 10K series e 50GB de logs.
- Sentry Developer grátis: 5K eventos/mes.
- Supabase inclui metricas no plano gratuito.

Leia `references/cost-overview.md` para uma comparacao detalhada.

## Checklist pre-deploy

Antes de colocar um servico em producao, valide a observabilidade. Use `references/pre-deploy-checklist.md` para nao esquecer nenhum pilar.

## Referencias da skill

Consulte estes documentos para templates, snippets e checklists extensos:

- `references/nextjs-otel.md`: instrumentacao OTel em Next.js.
- `references/python-otel.md`: instrumentacao OTel e logs JSON em Python.
- `references/health-check-examples.md`: exemplos de endpoints `/health`.
- `references/docker-compose-healthcheck.md`: configuracao de health checks em containers.
- `references/pre-deploy-checklist.md`: checklist completo antes do deploy.
- `references/cost-overview.md`: resumo de custos e tiers gratuitos.
