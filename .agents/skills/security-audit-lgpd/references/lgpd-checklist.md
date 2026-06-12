# Checklist LGPD para projetos Atomica

## Marco regulatório aplicável

A LGPD (Lei 13.709/2018) exige do agente de tratamento: finalidade específica, necessidade, transparência, segurança, prevenção e responsabilização. O titular deve ter acesso facilitado às informações sobre o tratamento.

Para software com IA, sete pontos são operacionalmente críticos:

1. **Registro das operações de tratamento** (art. 37).
2. **RIPD** em casos de alto risco, podendo a ANPD exigi-lo (art. 38).
3. **Medidas técnicas e administrativas** de segurança (art. 46).
4. **Notificação de incidente** relevante à ANPD e aos titulares (art. 48).
5. **Boas práticas e governança** (art. 50).
6. **Encarregado** designado; o alívio para pequeno porte cai quando há tratamento de alto risco.
7. **Atendimento aos direitos do titular** (art. 18).

O **art. 20** da LGPD garante ao titular o direito de solicitar revisão de decisões tomadas unicamente com base em tratamento automatizado que afete seus interesses. A prudência recomenda **human override** para decisões automatizadas com impacto relevante em direitos, acesso, crédito, emprego, reputação ou elegibilidade.

## Checklist de produção

| Controle | O que checar | Evidência mínima aceitável |
|---|---|---|
| Inventário de dados | Fontes, categorias de dados, fluxos, finalidades, operadores/suboperadores e países envolvidos | Mapa de dados + registro das operações por fluxo |
| Base legal por fluxo | Hipótese legal por processo; não use consentimento como muleta universal | Matriz “fluxo → finalidade → base legal → justificativa”; se usar legítimo interesse, faça teste de balanceamento e reforce transparência e registro; ele **não** serve para dados sensíveis |
| Transparência | Titular precisa entender o que é coletado, por quê, com quem é compartilhado e como exercer direitos | Política de privacidade versionada + aviso contextual nas telas/formulários/workflows |
| Direitos do titular | Processos para confirmação, acesso, correção, eliminação, portabilidade, revogação e oposição | Runbook interno + SLA + telas ou canal dedicado |
| Retenção e descarte | Dados eliminados após o término do tratamento, salvo hipóteses legais de conservação | Tabela de retenção por dataset + rotina automática de exclusão/anonimização |
| Encarregado | Responsável e canal de contato formalizados | Ato formal de designação + página/canal público de contato |
| RIPD | Em IA com alto risco, dados sensíveis, larga escala, profiling forte ou decisões automatizadas relevantes, trate RIPD como padrão interno | RIPD com riscos, salvaguardas e mitigação |
| Tratamento automatizado | Se a IA toma decisão que afeta interesses do titular, ofereça revisão e explicação dos critérios/procedimentos | Política de human override + canal de contestação + trilha de decisão |
| Transferência internacional | Mapeie país de destino e base da transferência; para UE↔Brasil, aproveite a adequação reconhecida em 2026, mas registre o fluxo | DPA/SCC quando aplicável + inventário de suboperadores + registro do mecanismo usado |
| Incidentes | Contenção, coleta de evidências, classificação e comunicação regulatória | Plano de resposta a incidente + responsáveis + modelos de comunicação ANPD/titulares |

## Regras operacionais Atomica

Além do texto legal, adote estas quatro regras internas para reduzir risco e facilitar auditoria:

1. **Não envie PII bruta para prompt** se for possível pseudonimizar, resumir ou tokenizar antes.
2. **Não ret prompts e outputs por padrão**; retenha apenas o que tiver finalidade defensável.
3. **Não deixe modelo ou agente executar ação destrutiva sem aprovação humana** quando o fluxo afetar direitos do titular.
4. **Versionamento de política, prompt de sistema, conjunto de ferramentas do agente e lista de suboperadores** — sem isso, accountability vira fumaça.

## Convergência internacional

- **GDPR**: records of processing activities (art. 30) e DPIA quando houver provável alto risco (art. 35).
- **AI Act**: aplicação faseada; high-risk systems passam a ter maior parte das obrigações a partir de 2 de agosto de 2026. Chatbots, copilots e automações de marketing tendem a cair primeiro no eixo de transparência, salvo contextos regulados do Anexo III.
- **Brasil ↔ UE**: em 2026 houve reconhecimento mútuo de adequação, simplificando transferências, mas sem eliminar o dever de mapear suboperadores, contratos, finalidades, retenção e segurança.

## Resoluções ANPD em aberto

- **Resolução CD/ANPD nº 15/2024**: regulamenta comunicação de incidente de segurança, fixando **3 dias úteis** para comunicação à ANPD e aos titulares quando houver risco ou dano relevante.
- **Resolução CD/ANPD nº 19/2024**: regulamenta transferência internacional, detalhando cláusulas-padrão, normas corporativas globais e decisões de adequação.
