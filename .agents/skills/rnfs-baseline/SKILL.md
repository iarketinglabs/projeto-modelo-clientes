---
name: rnfs-baseline
description: Baseline de requisitos não-funcionais para projetos Atomica de automação com IA. Use esta skill sempre que iniciar um novo projeto, durante a Fase 1 (Arquitetura) para definir SLIs, SLOs, limites operacionais, segurança e compliance. Cobre disponibilidade, latência, backups, observabilidade, segurança, LGPD e restrições do stack (Next.js, Python, n8n, Supabase, Docker/Easypanel).
---

# RNFs Baseline — Processo Atomica

Define o baseline de Requisitos Não-Funcionais para projetos Atomica. O baseline é um **default forte** com override explícito por projeto — cada projeto responde: mantém, endurece ou relaxa, e por quê.

## Quando usar

- Fase 1 do processo Atomica: "Definir RNFs baseline"
- Início de qualquer projeto novo (após o Diagnóstico)
- Gate 1: preparar documentação para validação do Guardião (CISO)
- Antes de qualquer deploy em produção

## Princípios

1. **Separe caminho síncrono de assíncrono**: o que bloqueia o usuário (APIs, UI) tem limites rígidos de latência; o que é background (IA, scraping, ETL) usa fila + status + timeout.
2. **Default forte, override explícito**: o baseline já traz valores; o projeto documenta o que mudou e por quê.
3. **Evidência, não promessa**: cada RNF exige evidência de validação (teste de carga, drill de restore, dashboard).

## Baseline numérico

Use estes valores como ponto de partida. Para o template completo com tabela de overrides, leia [`references/baseline-template.md`](references/baseline-template.md).

| Tema | Baseline | Quando endurecer |
|---|---|---|
| **Disponibilidade** | SLO 99,9% (43 min/mês de erro) | 99,95% para receita crítica |
| **Latência API síncrona** | p95 ≤ 800 ms, p99 ≤ 2 s | p95 ≤ 500 ms para dashboards/fluxos de alta frequência |
| **UX Web (LCP)** | p75 ≤ 2,5 s | Páginas de aquisição/receita |
| **UX Web (INP)** | p75 ≤ 200 ms | — |
| **Timeout fim-a-fim** | 8 s (teto síncrono) | 3-5 s se UX crítica |
| **Retries** | Até 2, só operações idempotentes, backoff + jitter | — |
| **Throughput** | Teste de carga a 2x pico por 15 min | 3x pico para lançamentos |
| **Backup** | Diário + off-site | PITR com RPO ≤ 15 min, RTO ≤ 4 h |
| **TLS** | 1.3 default, 1.2 compat | mTLS para integrações sensíveis |
| **MFA** | Obrigatório para admins | Usuários finais em ações sensíveis |
| **RLS Supabase** | Obrigatório em tabelas com dados de usuário | — |
| **Secrets** | Nada em repo/imagem/browser | Rotação automática |
| **Logs** | JSON estruturado, 30 dias operacional, 180 dias auditoria | — |
| **Observabilidade** | OpenTelemetry, 4 golden signals, /health/live, /health/ready | — |
| **LGPD** | Minimização, pseudonimização, retenção limitada, plano de incidente | RIPD para alto risco |

## Fluxo de aplicação

1. **Preencher o template**: use [`references/baseline-template.md`](references/baseline-template.md) — preencha tier de criticidade, stack, dados tratados.
2. **Override por projeto**: para cada métrica, decida mantém/endurece/relaxa com justificativa.
3. **Registrar restrições do stack**: quotas do Supabase, modo n8n, limites do Easypanel.
4. **Preencher checklist de validação**: use [`references/checklist-pre-go-live.md`](references/checklist-pre-go-live.md) antes de qualquer deploy.
5. **Submeter ao Guardião**: o Gate 1 exige aprovação do CISO/cliente nos RNFs.

## Trade-offs (matriz de decisão)

Leia [`references/tradeoffs.md`](references/tradeoffs.md) para a matriz completa. Resumo:

- **Síncrono com IA** → UX simples, mas risco de timeout. Prefira **job assíncrono com status** para LLM/scraping/ETL.
- **SLO 99,9%** → bom equilíbrio. SLO 99,99% → muito mais custo e disciplina.
- **Backups diários** → barato, mas perde até 24 h. **PITR + drills** → RPO muito melhor.
- **Queue mode n8n** → melhor escala, mas adiciona Redis e complexidade.
- **Next.js multi-instância** → exige cache compartilhado e mesma `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`.

## Checklist pré-go-live

Antes de qualquer deploy em produção, verifique:

- [ ] Tier de criticidade e SLO alvo definidos e justificados
- [ ] Teste de carga em staging (2x pico, 15 min) com evidência
- [ ] Fluxo síncrono cabe no orçamento; o resto é assíncrono com status
- [ ] Timeouts explícitos em toda chamada remota; retries só em idempotentes
- [ ] Backup automatizado + restore testado (drill documentado)
- [ ] TLS 1.3, MFA admins, RLS Supabase, secrets centralizados
- [ ] Logs JSON estruturados, tracing OTel, health checks, alertas SLO
- [ ] Classificação LGPD: dados em prompts? minimização aplicada?
- [ ] Riscos residuais registrados com aprovador

## Referências

| Recurso | Conteúdo |
|---|---|
| [`references/baseline-template.md`](references/baseline-template.md) | Template completo em Markdown para preenchimento por projeto |
| [`references/tradeoffs.md`](references/tradeoffs.md) | Matriz de trade-offs: cada decisão e seu custo |
| [`references/checklist-pre-go-live.md`](references/checklist-pre-go-live.md) | Checklist de validação antes do deploy |
| [`directives/deep-researches/09-rnfs-baseline.md`](../../../directives/deep-researches/09-rnfs-baseline.md) | Deep research completo com fundamentação (ISO 25010, SRE, OWASP, AWS) |

## Restrições do stack Atomica (jun/2026)

- **Supabase Pro**: 250 GB egress, 8 GB DB disk, 100 GB storage, 2M Edge Function invocations, 500 Realtime connections
- **n8n queue mode**: workers com concorrência 10 (mín. 5); multi-main HA é Enterprise
- **Next.js self-hosted**: múltiplas instâncias exigem cache compartilhado e mesma encryption key
