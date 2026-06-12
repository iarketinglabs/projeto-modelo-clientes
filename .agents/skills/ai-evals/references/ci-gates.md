# CI Gates para AI Evals

Separe a suite em dois tempos: rápida no pull request, completa antes de release.

## Pull request — smoke suite

Rápida, barata e sem juízes caros salvo quando essencial.

- Happy path
- Input ambíguo
- Saída malformada
- Regra-limite (boundary condition)
- Caso adversarial conhecido

Foque em:
- JSON/schema válido
- Campos obrigatórios
- Regras de negócio críticas
- Asserts determinísticos baratos

## Release/full suite

Rode à noite ou em pipeline pré-release.

- Judge semântico em todas as dimensões relevantes
- Métricas de groundedness/faithfulness
- Comparação com baseline oficial
- Trajectory evals para agentes
- Amostra humana em casos de disagreement

## Regras de gate

| Tipo de falha | Gate |
| --- | --- |
| Formato inválido, parse error, schema inválido | Hard fail |
| Campo obrigatório ausente | Hard fail |
| Regra de negócio violada | Hard fail |
| Métrica semântica abaixo do threshold | Soft fail / revisão amostral até o juiz estar calibrado |
| Regressão em relação ao baseline | Bloqueio de release |

## Baselines

- Sempre tenha uma versão oficial de prompt/model/dataset marcada como baseline.
- Não compare runs soltos sem baseline.
- Regresse só métricas estáveis; métricas em calibração entram como alerta, não gate.
