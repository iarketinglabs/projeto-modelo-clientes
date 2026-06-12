# Template de Relatório de Stress Test

Copie este template e preencha após cada execução real.

```md
# Relatório de Stress Test

## Contexto
- Sistema:
- Commit / release:
- Ambiente:
- Ferramenta e versão:
- Janela do teste:
- Responsável:

## Objetivo
- Hipótese que o teste queria validar
- Capacidade-alvo
- Risco de negócio associado

## Escopo
- Endpoints / jornadas cobertos
- O que ficou fora do escopo
- Tipo de carga: baseline / stress / spike / soak / race / volume

## Configuração do workload
- Modelo: open / closed / hybrid
- Cenários:
- Duração por fase:
- Taxa / VUs por fase:
- Dataset:
- Estratégia de seed:
- Auth / sessão:
- Headers especiais:
- Idempotency-Key: sim/não

## Thresholds e invariantes
- p95:
- p99:
- taxa de erro:
- dropped_iterations:
- invariantes de negócio:
- critérios de fail do pipeline:

## Resultados
| endpoint/jornada | req/s | p95 | p99 | erro % | dropped_iterations | observação |
|---|---:|---:|---:|---:|---:|---|

## Frontend
- LCP:
- INP:
- CLS:
- TTFB:
- anomalias visuais/percebidas:

## Infra correlata
- CPU:
- memória:
- rede:
- conexões DB:
- pool wait:
- backlog de fila:
- workers saturados:

## Race conditions
- cenário:
- respostas aceitáveis observadas:
- respostas não aceitáveis observadas:
- duplicidade de negócio detectada?:

## Achados principais
- Gargalo principal
- Gargalo secundário
- Efeito colateral inesperado
- Limite operacional estimado

## Decisão
- Go / No-Go / Go with guardrails
- Limites temporários de produção
- Próximas correções priorizadas

## Artefatos
- summary.json / CSV / dashboard / traces / logs
- link do run no CI
- dashboards consultados
```

## Automação sugerida

- Use `handleSummary()` do k6 para gerar JSON.
- Transforme o JSON em Markdown em um passo simples de pipeline.
- Locust exporta CSV em headless; JMeter gera dashboard HTML; Artillery pode enviar para OTel.
