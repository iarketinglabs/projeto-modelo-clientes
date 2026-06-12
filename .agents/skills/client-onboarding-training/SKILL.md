---
name: client-onboarding-training
description: Processo de onboarding e treinamento do cliente para projetos Atomica. Use esta skill durante a Fase 5 (Segurança, Deploy & Onboarding) após o deploy. Cobre agenda de onboarding (1-2h), guia do usuário, checklist pré-onboarding, follow-ups (7/14/30 dias) e métricas de adoção.
---

# Client Onboarding & Training — Processo Atomica

Estrutura a entrega e o treinamento do cliente para garantir adoção bem-sucedida do sistema. Cobre desde a preparação pré-sessão até os follow-ups de 30 dias.

## Quando usar

- Fase 5 do processo Atomica: "Treinamento do cliente"
- Após deploy bem-sucedido e antes da entrega formal
- Gate 3: preparar evidências de onboarding para sign-off final
- Sempre que um novo usuário ou time precisar ser onboarded

## Estrutura da sessão de onboarding (1–2h)

### 1. Introdução e objetivos (10 min)
- Apresentar equipe do projeto e papéis (CSM, Campeão/PO, TI do cliente)
- Alinhar metas do onboarding
- Explicar o "momento aha" esperado

### 2. Visão geral do sistema (15 min)
- Demonstrar proposta de valor e arquitetura
- Mostrar fluxos principais e funcionalidades-chave em ação
- Usar analogias familiares ao negócio do cliente

### 3. Demonstração prática (30 min)
- Walkthrough de um caso de uso típico até o cliente ver valor
- Ex.: enviar a primeira campanha, gerar o primeiro relatório
- Deixar o Campeão operar sob orientação (sandbox)

### 4. Hands-on e Q&A (30 min)
- Campeão testa funcionalidades com cenários reais do negócio
- Tirar dúvidas em tempo real
- Usar linguagem simples e analogias

### 5. Entregar documentação (10 min)
- Mostrar guia do usuário/README
- Destacar checklist inicial, FAQ e vídeos
- Garantir que o Campeão saiba usar a documentação como referência

### 6. Próximos passos (15 min)
- Definir primeiros marcos e canais de suporte
- Explicar follow-ups (7, 14, 30 dias)
- Alinhar expectativas de resposta e escalação

## Checklist pré-onboarding

Antes da sessão, confirme:

- [ ] **Preparação do cliente**: questionário prévio preenchido (metas, casos de uso prioritários)
- [ ] **Agenda e comunicação**: enviada por e-mail com tópicos e perguntas-chave
- [ ] **Acessos e dados**: contas criadas, permissões de admin, dados iniciais importados
- [ ] **Ambiente de treinamento**: sandbox ou ambiente separado configurado
- [ ] **Recursos e documentação**: guias de início rápido compartilhados antecipadamente

## Guia do usuário (estrutura recomendada)

Crie um README/guia com:

1. **Visão geral**: resumo do sistema, objetivos, propostas de valor
2. **Configuração inicial**: passo a passo com screenshots (criação de conta, permissões, login)
3. **Fluxo de uso básico**: tutorial guiado do primeiro caso de uso
4. **Integrações essenciais**: como conectar CRM, ERP, etc.
5. **FAQs e troubleshooting**: perguntas comuns, erros típicos, glossário
6. **Canais de suporte**: contatos, base de conhecimento, como abrir chamados

Use [`references/user-guide-template.md`](references/user-guide-template.md) como ponto de partida.

## Follow-ups pós-onboarding

| Prazo | Ação |
|---|---|
| **7 dias** | Check-in rápido: acessou? entendeu o básico? primeira ação concluída? Se não, reengajar. |
| **14 dias** | Reforçar funcionalidades não usadas, compartilhar boas práticas, pedir feedback. |
| **30 dias** | Reunião de validação: objetivos alcançados? NPS/CSAT. Métricas de uso. Sugestões. |

## Métricas de adoção (framework)

Monitore estes indicadores após o onboarding:

| Métrica | Baseline / Benchmark |
|---|---|
| **Tempo para Valor (TTV)** | Quanto menor, melhor. Medir até a primeira ação de valor. |
| **Taxa de Ativação** | ~37% média B2B SaaS; ~54,8% em IA/ML |
| **Regra dos 7%** | ≥7% dos usuários voltam no 7º dia → boa adoção inicial |
| **Features-chave** | Uso consistente das funcionalidades críticas |
| **Retenção/Churn** | Churn >98% se não vê valor nas primeiras 2 semanas |
| **DAU/MAU** | Usuários ativos vs licenças contratadas |
| **NPS/CSAT** | Medir aos 30 dias |

## Anti-padrões

- **Onboarding único e sem follow-up**: cliente abandona após a primeira semana
- **Documentação genérica**: sem screenshots, sem passos específicos do projeto
- **Só o Campeão participa**: outros usuários-chave ficam sem contexto
- **Sem métricas de adoção**: não sabe se o cliente está usando ou não
- **Suporte reativo**: esperar o cliente pedir ajuda em vez de fazer check-ins proativos

## Referências

| Recurso | Conteúdo |
|---|---|
| [`references/user-guide-template.md`](references/user-guide-template.md) | Template de guia do usuário/README |
| [`references/onboarding-agenda.md`](references/onboarding-agenda.md) | Agenda detalhada da sessão |
| [`references/follow-up-calendar.md`](references/follow-up-calendar.md) | Calendário de follow-ups com scripts de email |
| [`directives/deep-researches/11-client-onboarding-training.md`](../../../directives/deep-researches/11-client-onboarding-training.md) | Deep research completo com frameworks e benchmarks |
