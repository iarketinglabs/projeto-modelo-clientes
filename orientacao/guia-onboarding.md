# Guia de Onboarding — Iniciando um Projeto de Cliente

> **Para:** Membros da equipe Atômica que vão iniciar um novo projeto.
> **Pré-requisito:** Ter lido `orientacao/sobre-o-template.md`.

---

## Checklist Rápido

- [ ] Clonei este repositório
- [ ] Criei o repo GitHub do cliente
- [ ] Preenchi o `.env`
- [ ] Li o processo em `directives/atomica-processos.csv`
- [ ] Iniciei a Fase 0 (Diagnóstico)
- [ ] Substituí os placeholders em `directives/`

---

## 1. Setup Inicial (10 min)

```bash
# 1. Clone este template
git clone git@github.com:iarketinglabs/projeto-modelo-clientes.git nome-do-cliente
cd nome-do-cliente

# 2. Desconecte do repo template e crie o repo do cliente
rm -rf .git && git init

# 3. Crie o repo no GitHub (use o token do .env)
# Nome sugerido: [cliente]-[projeto] (ex: acme-crm-automation)
```

### 1.1 Configure o `.env`

```env
REPOSITORY_NAME=nome-do-cliente-projeto
GITHUB_OWNER=iarketinglabs
GITHUB_TOKEN_REPO_PROJ=ghp_...
GITHUB_TOKEN_NEW=ghp_...
```

> ⚠️ **Nunca commite o `.env`!** Ele já está no `.gitignore`.

---

## 2. Fase 0: Diagnóstico (2-5 dias)

Antes de escrever uma linha de código, complete o diagnóstico:

1. **Firmografia**: Tamanho da empresa, vertical, tech stack atual
2. **Dor operacional**: Quantas horas/semana perdidas em tarefas manuais?
3. **Gatilhos de urgência**: Por que agora?
4. **Métrica de sucesso**: Baseline numérica (ex: "de 15h para 2h/semana")
5. **Delegação Humano vs IA**: O que permanece humano?
6. **Stack do cliente**: Própria ou stack Atômica?
7. **Deal breakers**: ICP negativo? Recuse se for o caso.

**Skills relevantes:** brainstorming, business-analyst, xlsx

Os achados vão para o Documento de Diagnóstico (criar com `docx` ou `pptx`).

---

## 3. 🚪 Gate 0: Kickoff

Reunião com **Decisor + Campeão + Guardião**:

- Apresentar Documento de Diagnóstico
- Alinhar escopo, prazo e investimento
- Definir governança (quem é quem)
- **Decisor aprova formalmente**

**Skills:** pptx, docx, business-manager

---

## 4. Fase 1: Arquitetura & Planejamento (3-7 dias)

### 4.1 Preencha os placeholders em `directives/`

> ⚠️ **Importante:** Os arquivos em `directives/` contêm mensagens de orientação.
> Substitua cada um pelo conteúdo do projeto do cliente.

| Arquivo | O que preencher | Skill/Agent |
|---------|-----------------|-------------|
| `directives/PRD.md` | PRD Agentive do projeto (6 levas de entrevista) | `prd-creator` + agent:prd-engineer |
| `directives/architecture.md` | Arquitetura técnica (APIs, MCP, serviços) | `architecting-mcp-systems` + `ai-engineer` |
| `directives/brand_voice.md` | Tom de voz do cliente (se aplicável) | `brand-identity` |

### 4.2 Checklist da Fase 1

- [ ] PRD Agentive criado
- [ ] Especificações SDD escritas (cenários Dado/Quando/Então)
- [ ] Wireframes/protótipos (se aplicável)
- [ ] Arquitetura definida e documentada
- [ ] Stack final decidida (cliente ou Atômica)
- [ ] Agentes do projeto criados em `.agents/agents/`
- [ ] Checklist LGPD + compliance preenchido
- [ ] Modelagem de ameaças (Zero Trust)
- [ ] SBOM inicial gerado
- [ ] Supabase configurado
- [ ] `.env` preenchido com tokens do projeto
- [ ] RNFs baseline documentados

### 4.3 🚪 Gate 1

- Guardião (CISO) aprova stack e arquitetura
- Validação de segurança e compliance
- Sign-off do SBOM

---

## 5. Fase 2: Skills & Conhecimento (2-5 dias)

- [ ] Deep Research executado para cada competência
- [ ] Skills criadas em `.agents/skills/`
- [ ] LLM Routing configurado (Large/Medium/Small)

---

## 6. Fase 3: Desenvolvimento MVP (1-16 semanas)

- [ ] TDD onde aplicável
- [ ] CI/CD ativo (GitHub Actions)
- [ ] Dogfooding (se aplicável)
- [ ] Frontend (Next.js)
- [ ] Automações (Python / n8n)
- [ ] MVP funcional em `executions/`

---

## 7. Fase 4: QA & Validação (3-7 dias)

- [ ] Teste de estresse com IA
- [ ] Simulações manuais
- [ ] QA com evals (LLM-as-Judge)
- [ ] Verificação cross-model
- [ ] Bugs corrigidos

### 🚪 Gate 2: MVP

- Campeão testa e aprova
- Validação contra baseline do diagnóstico

---

## 8. Fase 5: Deploy & Onboarding (3-5 dias)

- [ ] Security review + OWASP
- [ ] SBOM final
- [ ] Repo GitHub privado + secrets
- [ ] CI/CD pipeline (GitHub Actions + Easypanel)
- [ ] Deploy Easypanel + Hostinger DNS
- [ ] Observabilidade configurada
- [ ] Treinamento do cliente

### 🚪 Gate 3: Entrega Final

- Decisor assina aceitação
- Guardião aprova segurança
- Documentação completa entregue

---

## 9. Fase 6: Retrospectiva (2-3 dias)

- [ ] Retrospectiva dos 3 sócios
- [ ] Skills reutilizáveis → biblioteca Atômica
- [ ] Processo atualizado com lições aprendidas
- [ ] Wrap-up

---

## Referências Rápidas

| Recurso | Local |
|---------|-------|
| Processo completo (CSV) | `directives/atomica-processos.csv` |
| Framework DOE | `orientacao/sobre-o-template.md` |
| Manifesto do agente | `.agents/agents.md` |
| PRD do cliente (placeholder) | `directives/PRD.md` |
| Arquitetura do cliente (placeholder) | `directives/architecture.md` |
| Brand voice do cliente (placeholder) | `directives/brand_voice.md` |

---

*Última atualização: 2026-06-12 | Atômica*
