# Report Template: Cross-Model Divergence

Use this template to document every cross-model verification run. A complete report makes the experiment reproducible and the decision defensible.

## Escopo

- Janela avaliada:
- Ambiente: staging / produção / shadow
- Modelos comparados:
  - Primário:
  - Secundário:
  - Juiz(es):
- IDs exatos dos modelos:
- Prompt / versão do workflow:
- Ferramentas habilitadas:
- Schema de saída:
- Data do relatório:
- Owner:

## Composição do dataset

- Total de casos:
- Por domínio:
- Por risco:
- Por idioma:
- Por canal:
- Por formato:
- Casos com referência:
- Casos sem referência:

## Métricas principais

| Métrica | Valor | Slice com maior gap |
|---|---|---|
| Structural failure rate | | |
| Agreement rate | | |
| Semantic divergence rate | | |
| Judge order stability | | |
| Critical divergence rate | | |
| Consensus error rate | | |
| Win/tie/loss (A vs B) | | |
| Confidence gap proxy (médio) | | |

## Divergências críticas

### Caso {{id}}

- Prompt resumido:
- Domínio / risco / slice:
- Output modelo A:
- Output modelo B:
- Veredito do júri:
- Impacto downstream:
- Causa provável:
- Ação recomendada:
- Owner:
- Prazo:

Repita o bloco acima para cada caso crítico.

## Padrões observados

- Tendência de recusa:
- Tendência de verbosidade:
- Tendência de alucinação / citações inventadas:
- Tendência por slice sensível:
- Tendência por idioma:
- Tendência por formato (JSON vs texto livre):

## Decisão

- Liberar / bloquear / shadow-only / roteamento parcial
- Mudanças exigidas:
- Casos que entram no golden set:
- Casos que entram no bias set:
- Casos que entram no edge set:
- Próxima data de reavaliação:

## Apêndice

- Link para o dataset:
- Link para os traces:
- Link para o código do harness:
- Notas de metodologia:
