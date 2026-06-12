---
name: security-audit-lgpd
description: Conduct security audits and LGPD compliance reviews for the Atomica stack (n8n, Python, Next.js, Supabase, AI agents). Use whenever the user mentions security audit, LGPD compliance, privacy review, threat modeling, Zero Trust, OWASP, AI governance, risk assessment, RIPD, data inventory, incident response, or access-control review for automations and AI agents. Also trigger for pre-production security gates, vulnerability scans, secrets leakage, RLS policies, webhook authentication, and AI-agent safeguards.
---

# Auditoria de Segurança e Compliance LGPD para a Atomica

## O que esta skill faz

Guia uma auditoria estruturada de segurança e privacidade para projetos Atomica construídos em cima de n8n, Python, Next.js, Supabase e agentes de IA. Conecta obrigações da LGPD brasileira a controles técnicos, modelagem de ameaças OWASP/STRIDE, comandos de scan e um playbook de resposta a incidentes.

A LGPD é principiológica, não prescritiva: o mesmo controle pode atender deveres de accountability, transparência, segurança e resposta a incidentes. Tratar LGPD + segurança + governança de IA como um único sistema de controle mantém a auditoria prática e evita teatro de checkbox.

## Quando usar esta skill

- Antes de colocar em produção qualquer fluxo que trate dados pessoais ou use IA.
- Quando o usuário pedir uma auditoria de segurança, revisão de LGPD, RIPD, avaliação de impacto à privacidade ou DPIA.
- Quando for construir modelos de ameaça para agentes de IA, APIs, webhooks ou bancos de dados.
- Após suspeitas de vazamento, brecha ou misconfiguração.
- Quando for endurecer a stack: RLS, segredos, CSP, webhooks, scan de dependências, guardrails de IA.

## Fluxo de auditoria

1. **Defina o escopo do sistema**
   - Liste os componentes: n8n, serviços Python, Next.js, Supabase, provedores de IA, vector stores, terceiros.
   - Identifique fluxos de dados, atores, fronteiras de confiança e suboperadores por país.

2. **Mapeie os dados pessoais**
   - Monte um inventário de dados com origem, categoria, finalidade, base legal, retenção e rotina de exclusão.
   - Veja [`references/lgpd-checklist.md`](./references/lgpd-checklist.md) para o checklist completo de produção.

3. **Modele as ameaças**
   - Use STRIDE para segurança, LINDDUN para privacidade e OWASP GenAI/Agentic para riscos específicos de IA.
   - Veja [`references/threat-modeling-template.md`](./references/threat-modeling-template.md).

4. **Verifique controles por camada**
   - Frontend, APIs, webhooks, Supabase, n8n, agentes de IA.
   - Veja [`references/owasp-baseline.md`](./references/owasp-baseline.md).

5. **Execute scans**
   - Dependências, containers, código e segredos.
   - Veja [`references/scan-commands.md`](./references/scan-commands.md).

6. **Documente gaps e um plano de remediação**
   - Risco, dono, evidência, prazo.

7. **Prepare a resposta a incidentes**
   - Veja [`references/incident-playbook.md`](./references/incident-playbook.md) para cronogramas e passos de notificação da LGPD.

## Princípios centrais

- **Menor privilégio**: cada papel, chave, ferramenta e agente deve acessar apenas o que precisa.
- **Negação por padrão**: tabelas sem RLS, webhooks sem autenticação e agentes sem allowlist de ferramentas são bloqueadores de deploy.
- **Privacidade desde o design**: colete o mínimo, pseudonimize antes de enviar para prompts e exclua quando a finalidade terminar.
- **Accountability via versionamento**: versione prompts, mensagens de sistema, listas de ferramentas, políticas e suboperadores.
- **Revisão humana**: decisões automatizadas que afetem direitos, crédito, emprego ou elegibilidade precisam de revisão humana.
- **Zero Trust**: nenhuma confiança baseada apenas em rede ou localização; autentique e autorize cada requisição a cada recurso.

## Checklist LGPD (resumo)

| Controle | Evidência mínima |
|---|---|
| Inventário de dados | Mapa de fontes, categorias, fluxos, operadores/suboperadores e países |
| Base legal por fluxo | Matriz: fluxo → finalidade → base → justificativa |
| Transparência | Política de privacidade versionada + aviso contextual |
| Direitos do titular | Runbook interno + SLA + canal de atendimento |
| Retenção e descarte | Tabela de retenção + exclusão ou anonimização automatizada |
| Encarregado | Ato formal de designação + canal público de contato |
| RIPD | Padrão para IA de alto risco, dados sensíveis, profiling ou decisões automatizadas relevantes |
| Decisões automatizadas | Política de human override + canal de contestação + trilha de decisão |
| Transferências internacionais | DPA/SCC quando aplicável + inventário de suboperadores + registro do mecanismo |
| Incidentes | Plano de resposta + responsáveis + modelos de comunicação ANPD/titulares |

Para o checklist completo e as regras operacionais Atomica, leia [`references/lgpd-checklist.md`](./references/lgpd-checklist.md).

## Baseline OWASP/STRIDE (resumo)

| Camada | Riscos principais | Controles baseline |
|---|---|---|
| Next.js | XSS, vazamento de segredos, clickjacking | CSP em `next.config.js`, nenhum segredo de servidor no bundle cliente, `NEXT_PUBLIC_*` restrito |
| APIs / Python | Autenticação quebrada, BOLA, SSRF, injection | Autorização a nível de objeto/propriedade, rate limits, validação de schema, controles de SSRF |
| Supabase | Bypass de RLS, elevação de privilégio | RLS em todas as tabelas expostas ao cliente, grants mínimos, service keys apenas server-side, SSL |
| Webhooks / n8n | Gatilhos não autenticados, retenção de dados | Autenticação em todo webhook, `N8N_ENCRYPTION_KEY`, pruning/redaction de execuções, external secrets |
| Agentes de IA | Prompt injection, excessive agency, tool misuse | Tool allowlist, scopes por ferramenta, separação leitura/escrita, aprovação humana para ações destrutivas, kill switch |

Para a baseline completa, leia [`references/owasp-baseline.md`](./references/owasp-baseline.md).

Para um template reutilizável de modelagem de ameaças, leia [`references/threat-modeling-template.md`](./references/threat-modeling-template.md).

## Ferramentas e comandos de scan

Execute pelo menos estas classes de scan no CI:

- **Dependências**: `npm audit`, `pip-audit`, `osv-scanner scan .`
- **Filesystem / containers / SBOM**: `trivy fs .`, `trivy image ...`, `syft dir:.`, `grype sbom:sbom.json`
- **Código e segredos**: `semgrep scan --config "p/default"`, `gitleaks dir -v .`, `gitleaks git`

Falhe builds em segredo exposto, service key em código cliente, CVE crítico sem justificativa formal, tabela exposta sem RLS, webhook de produção sem autenticação ou ausência de SBOM em release candidate.

Para a lista completa de comandos e critérios de aceite do CI, leia [`references/scan-commands.md`](./references/scan-commands.md).

## Playbook de resposta a incidentes (resumo)

1. **Conter**: isolar componente afetado, rotacionar chaves comprometidas, desabilitar webhooks maliciosos.
2. **Avaliar**: identificar dados pessoais envolvidos, escopo da exposição, titulares afetados e probabilidade de dano.
3. **Preservar evidências**: logs, snapshots, linha do tempo; restrinja acesso aos investigadores.
4. **Classificar**: incidente relevante quando houver risco ou dano a dados pessoais ou privacidade.
5. **Notificar**: ANPD e titulares afetados em até **3 dias úteis** quando o incidente for relevante (Resolução CD/ANPD nº 15/2024).
6. **Remediar**: corrigir causa raiz, atualizar controles, re-executar scans.
7. **Documentar e aprender**: relatório pós-incidente, atualização de runbooks, revisão de retenção e acessos.

Para o playbook completo, leia [`references/incident-playbook.md`](./references/incident-playbook.md).

## Template de saída

Quando solicitado um relatório de auditoria, produza:

```markdown
# Auditoria de Segurança e LGPD — [projeto/fluxo]

## Resumo executivo
- Escopo, dados tratados, nível de risco, recomendação de go/no-go.

## Inventário de dados e base legal
- Fontes, categorias, finalidades, bases, retenção, suboperadores.

## Modelagem de ameaças
- Atores, fronteiras de confiança, riscos STRIDE/LINDDUN/GenAI, controles, gaps.

## Achados por camada
- Next.js, APIs, Supabase, n8n, agentes de IA.

## Resultados de scan
- Ferramentas executadas, achados, severidade, remediação.

## Plano de remediação
- Prioridade, dono, evidência necessária, prazo.

## Preparação para incidentes
- Alinhamento com playbook e obrigações de notificação.
```

## Arquivos de referência

- [`references/lgpd-checklist.md`](./references/lgpd-checklist.md) — checklist completo LGPD e regras operacionais Atomica.
- [`references/owasp-baseline.md`](./references/owasp-baseline.md) — baseline de segurança por camada e OWASP.
- [`references/threat-modeling-template.md`](./references/threat-modeling-template.md) — template STRIDE/LINDDUN/GenAI para agentes de IA.
- [`references/scan-commands.md`](./references/scan-commands.md) — comandos de scan de dependências, containers, código e segredos.
- [`references/incident-playbook.md`](./references/incident-playbook.md) — playbook de resposta a incidentes e SLA de notificação.
