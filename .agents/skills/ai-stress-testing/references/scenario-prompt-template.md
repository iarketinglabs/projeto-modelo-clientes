# Template de prompt para matriz de cenários

Use este prompt para gerar a matriz de cenários antes de pedir qualquer script.

```txt
Você é um arquiteto de testes de stress.

Objetivo:
Criar uma matriz de cenários reproduzíveis para k6, Artillery e Locust.

Contexto fixo:
- Stack: Next.js, Python, n8n, Supabase, APIs REST
- Ambiente-alvo: staging
- Fontes da verdade: OpenAPI, exemplos de requests reais, limites documentados do sistema
- Ferramentas preferidas: k6 como padrão, Artillery para browser, Locust apenas se Python fizer mais sentido
- Política: não inventar endpoints, headers, auth nem campos
- Critérios de saída: JSON válido seguindo exatamente o schema abaixo

Entradas:
<openapi_spec>
{{colar spec ou resumo}}
</openapi_spec>

<riscos_de_negocio>
- duplicate submit
- duplo clique
- concorrência sobre mesmo recurso
- webhook duplicado
- importação 10k+ registros
- leitura/paginação/export sobre 1M+ itens
- concurrent sessions
- workflow order bypass
</riscos_de_negocio>

<slo_inicial>
- p95 por endpoint crítico
- p99 global
- erro máximo aceitável
- dropped iterations aceitáveis
- zero duplicidade de negócio
</slo_inicial>

<schema_saida_json>
{
  "scenarios": [
    {
      "name": "string",
      "tool": "k6|artillery|locust",
      "layer": "api|browser|workflow|db_pool",
      "traffic_model": "open|closed|hybrid",
      "goal": "baseline|stress|spike|soak|race|volume",
      "target_endpoints": ["string"],
      "same_identity": true,
      "dataset_strategy": "seeded|csv|generated",
      "dataset_size": "string",
      "concurrency_pattern": "string",
      "phases": [
        { "duration": "string", "rate_or_vus": "string" }
      ],
      "assertions": ["string"],
      "business_invariants": ["string"],
      "metrics_to_watch": ["string"],
      "failure_thresholds": ["string"]
    }
  ]
}
</schema_saida_json>

Regras:
- Produza no mínimo 8 cenários e no máximo 14
- Inclua pelo menos 2 cenários de race condition
- Inclua pelo menos 2 cenários de volume extremo
- Marque quais exigem massa pré-semeada
- Marque quais precisam de mesma identidade/session/token
- Não gere script ainda
```

## Prompt para geração de script

Após aprovar a matriz, use este prompt para gerar o script executável.

```txt
Você vai gerar um script k6 pronto para rodar.

Entrada:
- Cenário aprovado em JSON
- OpenAPI resumida
- Base URL, auth e headers válidos
- Endpoints permitidos
- SLOs e thresholds

Regras obrigatórias:
- Use apenas APIs oficiais do k6
- Não invente endpoint nem status code esperado
- Parametrize BASE_URL e credentials com __ENV
- Inclua scenarios, thresholds, checks, tags e handleSummary
- Identifique endpoints críticos com tags
- Se houver race condition, use batch/paralelismo explícito
- Se houver volume, separe setup/seed de medição
- Retorne:
  1) arquivo completo
  2) comando de execução
  3) quais variáveis de ambiente são obrigatórias
  4) quais invariantes de negócio o script valida
```

## Prompt para pacote de race condition

```txt
Você vai gerar um pacote de testes de race condition.

Objetivo:
Detectar duplicate submit, replay, workflow order bypass e concorrência sobre mesmo recurso.

Restrições:
- A mesma identidade deve ser reutilizada quando o risco exigir
- O mesmo recurso deve ser atacado por múltiplas requests quase simultâneas
- Explique quais respostas contam como aceitáveis:
  - created once + conflicts/duplicates depois
  - created once + replay idempotente com mesma resposta
- Explique quais respostas contam como falha:
  - duas criações de negócio
  - duas cobranças
  - dois coupons consumidos
  - dois estados finais incompatíveis

Saída:
- script executável
- lista de invariantes de banco/negócio a validar
- tabela curta "status aceitável vs status não aceitável"
```
