---
name: ai-stress-testing
description: Use this skill whenever the user asks for stress testing, load testing, performance testing, spike testing, soak testing, race condition testing, or AI-assisted stress testing for Next.js + Python + n8n + Supabase stacks. Trigger on mentions of k6, Artillery, Locust, JMeter, load test, stress test, spike, soak, race condition, concurrent sessions, duplicate submit, workflow order bypass, webhook replay, volume test, capacity test, p95/p99 thresholds, dropped iterations, or when preparing a pre-deploy performance gate. Use before generating any load test script, CI workflow, or stress report.
---

# AI Stress Testing

Guia prático para projetar, gerar e operar testes de stress com assistência de LLM em stacks **Next.js + Python + n8n + Supabase**.

O papel do LLM não é gerar carga em si, mas compilar contexto (OpenAPI, HAR, SLOs, riscos de negócio) em cenários reproduzíveis e scripts revisáveis como código.

## Quando usar esta skill

- Planejar matriz de cenários de carga (baseline, stress, spike, soak, race, volume).
- Escolher entre k6, Artillery e Locust para uma stack Next.js/Python/n8n/Supabase.
- Gerar scripts de stress, gates de CI e templates de relatório.
- Revisar thresholds, invariantes de negócio e checklists pré-deploy.

## Workflow recomendado

Siga esta ordem. Não pule a matriz para ir direto ao script: omissão de cenário é o erro mais comum.

1. **Colete entradas de verdade**
   - OpenAPI ou HAR real.
   - Headers, auth e regras de `Idempotency-Key`.
   - Limites documentados do sistema (pool size, workers, filas).
   - SLOs iniciais (p95, p99, erro máximo, dropped iterations).
   - Riscos de negócio (duplicate submit, duplo clique, webhook replay, workflow order bypass, concorrência sobre mesmo recurso).

2. **Gere a matriz de cenários**
   - Use o prompt de `references/scenario-prompt-template.md`.
   - Valide o JSON contra o schema antes de prosseguir.
   - Garanta pelo menos 8 cenários, sendo 2 de race condition e 2 de volume extremo.

3. **Gere scripts executáveis**
   - k6 como padrão para APIs e Route Handlers do Next.js.
   - Artillery para jornadas críticas de frontend com Playwright.
   - Locust apenas quando Python for mais natural (stateful, gRPC, SDK interno).
   - Parametrize tudo com variáveis de ambiente (`__ENV`, `process.env`).

4. **Execute dry-run e revisão humana**
   - Valide endpoints, status codes aceitáveis e semântica de negócio.
   - Confirme que massa de dados pré-semeada existe para cenários de 1M+ itens.

5. **Rode o teste real e colete métricas**
   - Use thresholds/ensure para falhar o pipeline.
   - Envie métricas para Prometheus/OpenTelemetry quando possível.

6. **Documente com o relatório padrão**
   - Use `references/report-template.md`.

## Matriz de cenários

Separe cenários por camada e objetivo. Evite misturar rotas cacheadas e dinâmicas do Next.js no mesmo pacote.

| Camada | Objetivo | Modelo de tráfego | Ferramenta típica |
|---|---|---|---|
| API REST / Route Handlers | baseline, stress, spike, soak | open (`ramping-arrival-rate`) | k6 |
| Frontend crítico | Web Vitals sob carga | closed/hybrid | Artillery + Playwright |
| Banco / pool de conexões | exaustão de pool, latência de espera | open | k6 |
| Workflow (n8n) | throughput de webhook, backlog de workers | open/closed | k6 ou Locust |
| Race condition | duplicate submit, replay, concorrência | closed/burst | k6 (`batch`) |
| Volume extremo | importação 10k+, leitura/export 1M+ | open | k6 |

**Regras de modelagem:**
- APIs de alta concorrência pedem modelo aberto (arrival rate).
- Jornadas humanas pedem modelo fechado (VUs fixos/rampados).
- Cenários de race precisam da mesma identidade/session/token atacando o mesmo recurso.
- Volume extremo exige massa pré-semeada; nunca gere 1M de itens no runner por iteração.

## Seleção de ferramentas

Use este mapa para escolher a ferramenta certa. A stack padrão do Atomica é **k6 para APIs, Artillery para frontend crítico, Locust para exceções Python**.

### k6 (padrão)

- Brilha em: APIs REST, Route Handlers, throughput, spike/soak, testes híbridos backend + browser.
- Vantagens: open-source, thresholds nativos, TypeScript habilitado, geração via OpenAPI, saída para Prometheus/OTel.
- Cuidado: browser load consome mais recursos; use coorte pequena.

### Artillery (complemento frontend)

- Brilha em: jornadas de frontend, Playwright em carga, WebSocket/Socket.IO, métricas por endpoint.
- Vantagens: YAML/TS/JS, `ensure`, `metrics-by-endpoint`, plugins `fake-data`/`fuzzer`, Web Vitals automáticos.
- Cuidado: não é a primeira escolha para throughput puro de API.

### Locust (exceção Python)

- Brilha em: simulações stateful em Python, gRPC, SDKs internos, times backend-first em Python.
- Vantagens: Python puro, `LoadTestShape`, execução distribuída master/worker, headless + CSV.
- Cuidado: gates de qualidade exigem mais código próprio; menos linear para stack JS.

### JMeter (legado)

- Use apenas quando já existir padrão organizacional forte ou acervo legado.
- A GUI serve só para montar/debugar; load real roda em CLI.

## Métricas essenciais

Divida o dashboard em três blocos.

### API / backend

- `http_req_duration` (p95, p99)
- `http_req_failed`
- `iterations`, `iteration_duration`
- `vus`, `vus_max`
- `dropped_iterations` — denuncia má configuração do executor ou saturação real
- Métricas customizadas de negócio (`business_failures`, `duplicate_creates`)

### Frontend

- LCP, FCP, INP, CLS, TTFB
- Contagem de status codes por página

### Infraestrutura

- CPU, memória, rede
- Conexões de banco e pool wait
- Fila/backlog e workers ocupados (n8n)
- Tempo de resposta de dependências

### Métricas específicas da stack

- **Supabase**: conexões diretas, pool size, tempo de espera por conexão.
- **n8n**: backlog em Redis, taxa de chegada de webhooks, workers ocupados, tempo de execução.
- **Next.js**: diferença entre rotas cacheadas e dinâmicas; `GET` cacheável pode mascarar gargalo de backend.

## Integração com CI/CD

Organize em camadas:

- **PR**: smoke/stress curto, focado em correção sob carga pequena.
- **Merge para main / deploy em staging**: baseline com rampa até o pico esperado.
- **Nightly**: stress e spike mais agressivos.
- **Semanal**: soak.

Ambos k6 e Artillery falham a execução quando thresholds ou `ensure` não passam. Locust entra via headless + CSV e validação própria em torno do resultado.

Use tags no k6 e `metrics-by-endpoint` no Artillery para evitar dashboards agregados que escondem a causa raiz.

## Gates de qualidade iniciais

Ajuste com histórico real, mas comece com:

- Erro HTTP < 1%.
- p95 por endpoint crítico dentro do SLO.
- p99 dentro da margem de degradação aceitável.
- `dropped_iterations` dentro de um orçamento pequeno e explícito.
- Zero duplicidade de negócio.
- Zero transição de estado inválida.
- Zero crescimento anormal de backlog/fila/workers sob carga sustentada.

## Arquivos de referência

Leia os arquivos abaixo conforme a etapa do workflow:

- `references/scenario-prompt-template.md` — prompt para gerar a matriz de cenários em JSON.
- `references/k6-examples.md` — exemplos de script k6 para stress de API e race condition.
- `references/artillery-example.md` — exemplo de Artillery + Playwright para frontend Next.js.
- `references/report-template.md` — template de relatório de stress test.
- `references/pre-deploy-checklist.md` — checklist de verificações antes do deploy.

## Dicas de operação

- Valide JSON schemas antes de gerar scripts. Isso reduz alucinação decorativa do LLM.
- Separe pacotes de teste para GET cacheado, GET dinâmico e POST/PATCH/DELETE.
- Para race conditions, teste com e sem `Idempotency-Key`.
- Não deixe o teste isolado na CLI: envie métricas para Prometheus/OpenTelemetry para correlacionar spike com traces e infra.
- Transforme resultados em artifact (JSON, CSV, dashboard), não apenas stdout.
