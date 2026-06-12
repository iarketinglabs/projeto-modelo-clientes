---
name: dogfooding-process
description: Processo de uso interno antes de entregar ao cliente. Use esta skill durante a Fase 3 (Desenvolvimento MVP) quando o sistema estiver funcional e antes do Gate 2 (MVP). Cobre planejamento, execução de 1 semana, coleta de feedback, critérios de saída e anti-padrões. Complementa — não substitui — o QA formal.
---

# Dogfooding Process — Processo Atomica

Processo de "comer a própria ração": usar internamente o sistema por ≥1 semana antes de mostrar ao cliente. Expõe problemas de usabilidade, bugs e gaps que só aparecem em uso real.

## Quando usar

- Fase 3 do processo Atomica: "Dogfooding condicional"
- Quando o MVP está funcional e cobre os Must have do PRD
- **Antes** do Gate 2 (apresentação ao Campeão/PO)
- Sempre que o sistema for similar a algo que a Atomica pode usar nos próprios processos

## Quando NÃO aplicar

- Scripts pontuais sem interface de usuário
- Integrações que dependem exclusivamente de dados do cliente
- Projetos onde o uso interno não é viável (ex.: sistema de folha de pagamento de outra empresa)

## Estrutura da semana de dogfooding

### Pré-planejamento

- [ ] Definir escopo: quais funcionalidades testar (ex.: agente de follow-up, dashboard)
- [ ] Garantir ambiente de produção ou staging-flag com todas as features
- [ ] Selecionar participantes: **não só devs** — incluir PM, suporte, vendas, etc.
- [ ] Criar canal único de feedback (documento共享 ou canal Slack dedicado)

### Dia 1: Kickoff

- [ ] Apresentar o sistema ao time (30 min)
- [ ] Fornecer documentação básica
- [ ] Explicar objetivo: usar como se já estivesse no cliente
- [ ] Mostrar fluxos críticos

### Dias 1–7: Uso real

- [ ] Cada participante usa o sistema nas tarefas diárias
- [ ] Registrar bugs e impressões no canal central
- [ ] Monitorar: logins, tempo de uso, performance, erros
- [ ] Não forçar — integrar ao trabalho normal

### Meio da semana: Checkpoint

- [ ] Reunião rápida de alinhamento (15 min)
- [ ] Identificar bugs críticos para correção imediata
- [ ] Ajustar rota se necessário

### Final da semana: Encerramento

- [ ] Reunião de feedback com todos os participantes
- [ ] Listar bugs e fricções, classificar por severidade (P0–P4)
- [ ] Priorizar correções para a semana seguinte

### Semana seguinte: Iteração

- [ ] Corrigir P0/P1
- [ ] Atualizar documentação/tutoriais com base no feedback
- [ ] Reavaliar contra critérios de saída

## O que observar

- **Bugs críticos**: erros que travam fluxos-chave ou geram dados incorretos
- **Fluxos principais**: testar ponta a ponta sem pular etapas
- **Usabilidade**: pontos de confusão, cliques sem resposta, texto truncado
- **Performance**: lentidão, travamentos, tempo de resposta
- **Fricção**: muitos cliques, campos repetidos, erros frequentes
- **Segurança**: controles de acesso, fluxos de exceção, logout

## Template de feedback

Cada bug/sugestão deve conter:

```markdown
- Título/ID: [referência única]
- Descrição: [texto claro do problema]
- Passos para reproduzir: [lista numerada]
- Resultado esperado vs obtido: [o que deveria vs o que aconteceu]
- Ambiente: [navegador, versão, conta]
- Severidade: P0/P1/P2/P3/P4
- Screenshots/logs: [anexos]
- Responsável: [quem investiga]
- Status: Aberto | Em andamento | Resolvido
```

## Critérios de saída (Pronto para Cliente)

Antes de levar ao cliente, todos estes devem ser **verdadeiros**:

- [ ] **Nenhum P0/P1 pendente** — bugs críticos resolvidos
- [ ] **Fluxos essenciais validados** — caminhos principais testados com sucesso
- [ ] **Performance aceitável** — dentro dos RNFs baseline
- [ ] **Satisfação interna** — NPS interno ≥ 4,4/5 ou time confortável
- [ ] **Documentação atualizada** — guias, tutoriais, onboarding revisados
- [ ] **Ambiente de produção preparado** — configurações de segurança e rollout definidas
- [ ] **Plano de mitigação** — rollback e correções rápidas documentadas

Se qualquer critério falhar, **adie o go-live e itere mais uma semana**.

## Anti-padrões

| Erro | Por que evitar |
|---|---|
| **Focar só em bugs** | Ignora insights de UX e adoção. Pergunte também "o que te frustrou?" |
| **Forçar como "segundo emprego"** | Gera resistência. Integre ao trabalho normal, mostre valor. |
| **Sem métricas** | Sem NPS, sem contagem de feedback, sem baseline — o processo não evolui. |
| **Só devs testando** | Onboarding, docs e fluxo de novato nunca são testados. Inclua não-técnicos. |
| **Feedback disperso** | 5 canais diferentes = feedback perdido. Centralize em UM lugar. |
| **Não agir sobre o feedback** | Time reporta e nada muda → participação morre. Mostre progresso. |
| **Ignorar onboarding** | Docs e tutoriais ficam stale. Revalide o fluxo de primeiro uso. |

## Referências

| Recurso | Conteúdo |
|---|---|
| [`references/checklist.md`](references/checklist.md) | Checklist detalhada de processo |
| [`references/exit-criteria.md`](references/exit-criteria.md) | Critérios de saída expandidos |
| [`references/feedback-template.md`](references/feedback-template.md) | Template de documento de feedback |
| [`directives/deep-researches/10-dogfooding-process.md`](../../../directives/deep-researches/10-dogfooding-process.md) | Deep research completo com cases (Microsoft, Apple, Slack, Intercom, Google Buzz) |
