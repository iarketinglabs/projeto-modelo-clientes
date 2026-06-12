# Criticality Criteria for Cross-Model Divergence

Use these rules to route each comparison to the right queue. The goal is to send only what matters to humans, not to review every stylistic difference.

## Critical immediately

A divergence is critical when it changes any of the following:

- Safety or compliance outcome.
- Legal, financial or health advice.
- Personal data handling or privacy decision.
- Commercial promise to a customer (price, deadline, feature, refund).
- Operational instruction that is hard to reverse (publish, send, charge, classify).
- Tool call, automation trigger or downstream action.
- Lead scoring or routing with business impact.
- One model refuses and the other complies.
- Structural field that drives a decision (label, category, priority, status).

## Critical by context

A divergence is critical when:

- The case is high-risk and the outputs are semantically different, even without a reference answer.
- The judge panel is unstable when candidate order is swapped.
- A slice gap appears for a sensitive group, language or domain.

## Not critical

A divergence is benign when it only affects:

- Style, tone or wording.
- Order of points.
- Level of detail or verbosity.
- Creativity or density.
- Formatting that does not change the structured meaning.

## Escalate to human

Escalate when:

- The judge panel ties on a high-stakes case.
- Order swap changes the verdict.
- Consensus feels suspicious in a sensitive case.
- Bias by slice is suspected.
- The confidence gap proxy is high but no single model is obviously wrong.

## Routing summary

| Situação | Fila | Ação |
|---|---|---|
| Baixo risco + equivalência semântica | Verde | Log only |
| Divergência reversível + risco médio | Amarela | Shadow monitor / roteamento secundário |
| Divergência material em alto risco | Vermelha | Revisão humana ou bloqueio |
| Instabilidade do juiz / empate sensível | Vermelha | Revisão humana |
