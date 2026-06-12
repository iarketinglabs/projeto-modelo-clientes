# PRD — Projeto Modelo (Template Base da Atômica)

> **Versão:** 1.0 | **Status:** Ativo | **Produto:** Template de workspace para agentes de IA

---

## 1. Visão do Produto

O **Projeto Modelo** é o template canônico da Atômica para inicialização de novos projetos. Ele padroniza a estrutura de diretórios, convenções de código, stack tecnológica default e — principalmente — o comportamento de agentes de IA que operam como executores autônomos dentro do workspace.

### 1.1 Problema que resolve

Cada novo projeto da Atômica (automação, conteúdo, APIs, ferramentas internas) exige um ponto de partida consistente. Sem um template, cada projeto divergia em estrutura, convenções e qualidade, gerando retrabalho e dificultando a portabilidade entre contextos.

### 1.2 Público-alvo

- **Primário:** Agentes de IA (Claude, GPT, Qwen Code) atuando como executores autônomos
- **Secundário:** Pedro (fundador) como operador humano e revisor
- **Terciário:** Novos colaboradores que precisam entender rapidamente a estrutura de qualquer projeto Atômica

---

## 2. Arquitetura: Framework DOE

O projeto adota o framework **DOE** — Diretivas, Orquestração, Execução — que separa responsabilidades em três camadas deterministicamente isoladas:

| Camada | Local | Responsabilidade | Restrição |
|--------|-------|------------------|-----------|
| **Diretivas** | `directives/` | SOPs, regras de negócio, PRDs em linguagem natural (Markdown) | **Zero código executável** |
| **Orquestração** | Agente + `.agents/` | Roteamento, decisão tática, escolha de ferramentas e skills | Sempre lê a diretiva antes de executar |
| **Execução** | `executions/` | Scripts atômicos e determinísticos (Python, JS, Shell) | **Uma única responsabilidade** por script |

### 2.1 Por que três camadas?

LLMs são probabilísticos por natureza; a lógica de negócio não pode ser. O framework DOE garante que:

- **Diretivas** documentam o "o quê" e o "porquê" de forma imutável durante a execução
- **Execuções** implementam o "como" de forma determinística e testável
- **Orquestração** (o agente) apenas conecta as duas pontas, sem conter lógica de negócio

---

## 3. Estrutura de Diretórios

```
projeto-modelo/
├── .agents/              # Configuração dos agentes de IA
│   ├── agents.md         # Manifesto de operação (system prompt do projeto)
│   ├── settings.json     # Configurações do agente
│   ├── mcps.json         # Servidores MCP conectados
│   ├── agents/           # Definições de sub-agentes
│   ├── commands/         # Comandos customizados
│   ├── hooks/            # Hooks de ciclo de vida
│   ├── rules/            # Regras aprendidas/adicionais
│   └── skills/           # Skills especializadas
├── directives/           # Diretrizes centrais (SOPs)
│   ├── PRD.md            # Este documento
│   ├── architecture.md   # Arquitetura do sistema
│   ├── brand_voice.md    # Voz da marca
│   └── updates.md        # Changelog de alterações
├── executions/           # Scripts determinísticos
│   └── outputs/          # Resultados persistentes de execuções
├── tmp/                  # Arquivos temporários (apagar após uso)
├── .env                  # Segredos e variáveis de ambiente
├── .gitignore            # Arquivos não versionados
└── README.md             # Documentação de entrada
```

### 3.1 Regras de convivência

- **`tmp/`**: Todo rascunho, arquivo intermediário ou teste vai aqui. Apagar após o uso.
- **`executions/outputs/`**: Se o resultado de um script deve persistir, salvar aqui.
- **Nova diretiva**: Se uma tarefa se tornar recorrente, criar `.md` em `directives/` — nunca documentar ad-hoc no chat.
- **`.env`**: Única fonte de segredos. Nunca hardcodar tokens ou senhas.

---

## 4. Stack Tecnológica Default

Se um novo projeto não especificar o contrário, estas são as escolhas canônicas:

| Camada | Tecnologia | Uso |
|--------|-----------|-----|
| **Scripts/Automação** | Python 3.11+ | Scripts determinísticos, integrações |
| **Web** | Next.js + Tailwind CSS | Frontend e APIs |
| **Banco de dados** | PostgreSQL (produção) / SQLite (protótipos) | Persistência |
| **Containerização** | Docker + Docker Compose | Deploy e orquestração de serviços |
| **Estilo de código** | Funcional quando possível; nomes em português ou inglês (manter consistência) | |
| **Design visual** | Minimalista (Apple-like), evitar poluição | |

---

## 5. Processo Atômica de Projetos

Todo projeto na Atômica segue um processo determinístico de **6 fases + 7 gates**, documentado em `directives/atomica-processos.csv`. Cada fase tem responsáveis, entregáveis e skills definidas.

### 5.1 Papéis e Responsabilidades

| Papel | Lado | Função |
|-------|------|--------|
| **Engagement Lead** | Atômica | Relacionamento com cliente, diagnóstico, alinhamento |
| **Tech Lead** | Atômica | Arquitetura, código, stack, segurança |
| **Delivery Manager** | Atômica | Cronograma, riscos, prazos |
| **Decisor** | Cliente | CEO/CFO/Founder — aprova gates, escopo e investimento |
| **Campeão** | Cliente | Product Owner — valida requisitos, testa aceitação |
| **Guardião** | Cliente | CISO/TI — aprova arquitetura, segurança e compliance |

### 5.2 Visão Geral das Fases

```
🚪 Gate -1 ──→ Fase 0 ──→ 🚪 Gate 0 ──→ Fase 1 ──→ 🚪 Gate 1
   Diagnóstico    (2-5d)      Kickoff       (3-7d)      Arquitetura
                                                      Aprova stack,
                                                      segurança, SBOM

Fase 2 ──→ Fase 3 ──→ Fase 4 ──→ 🚪 Gate 2 ──→ Fase 5 ──→ 🚪 Gate 3 ──→ Fase 6
(2-5d)     (1-16sem)   (3-7d)       MVP           (3-5d)      Entrega      (2-3d)
Skills     Desenv.     QA &       Aceitação      Segurança,   Final         Retrosp.
& Base     MVP         Validação   funcional     Deploy &                  Melhoria
                                             Onboarding                  Contínua
```

### 5.3 Detalhamento por Fase

#### 🚪 Gate -1: Diagnóstico
Reunião inicial para explicar os próximos passos e obter informações necessárias para construir o Diagnóstico.
- **Skills:** brainstorming, business-analyst

#### Fase 0: Diagnóstico (2-5 dias)
- Firmografia & Tecnografia (tamanho, vertical, tech stack do cliente)
- Mapeamento da dor operacional (horas perdidas em tarefas manuais)
- Identificação de gatilhos de urgência
- Definir métrica de sucesso com baseline numérica (ganho de tempo)
- Estratégia de delegação Humano vs IA
- Análise da stack do cliente (própria ou stack Atômica?)
- Estimativa de prazo do projeto (2 semanas a 4 meses)
- Identificar ICP negativo / deal breakers
- **Entregável:** Documento de Diagnóstico
- **Skills:** brainstorming, business-analyst, xlsx, ai-engineer, business-manager

#### 🚪 Gate 0: Kickoff
- Alinhamento de expectativas com cliente (Decisor + Campeão + Guardião + Atômica)
- Definir governança do projeto (3 papéis cliente + 3 papéis Atômica)
- Aprovação formal do escopo preliminar pelo Decisor
- **Skills:** pptx, docx, business-manager

#### Fase 1: Arquitetura, SDD & Planejamento (3-7 dias)
- Importar diretrizes e contexto do cliente (SOPs, planos, apresentações)
- Spec-Driven Development: escrever especificações orientadas a cenários
- Criar PRD Agentive (via PRD Engineer + entrevista em 6 levas)
- Criar Boneco UI/UX (wireframes e protótipos)
- Definir arquitetura de referência (API-first, MCP, vetores)
- Decidir stack final (Atômica ou do cliente)
- Criar agentes do projeto via System Prompt Engineer
- Checklist de compliance (LGPD + boas práticas IA)
- Modelagem de ameaças (Zero Trust, privilégio mínimo)
- Gerar SBOM inicial
- Setup do projeto: clonar projeto-modelo, renomear, abrir na IDE
- Configurar Supabase, preencher .env, tokens API
- Definir RNFs baseline (latência, uptime, backup, observabilidade)
- **Entregáveis:** PRD.md, Documento de Arquitetura, Wireframes, SBOM v1, Checklist Compliance
- **Skills:** prd-creator, writing-plans, frontend-design, mcp-builder, system-prompt-creator, security-audit-lgpd, sbom-generator, supabase-expert, rnfs-baseline
- **Agents:** prd-engineer, system-prompt-engineer

#### 🚪 Gate 1: Arquitetura
- Aprovação da stack e arquitetura pelo Guardião (CISO)
- Validação de segurança e compliance
- Sign-off do SBOM inicial

#### Fase 2: Skills & Base de Conhecimento (2-5 dias)
- Executar Deep Research por competência (Gemini, Kimi, ChatGPT)
- Listar competências e habilidades necessárias
- Criar skills em `.agents/skills/` (skill.md, references/, evals/)
- Transformar bases de conhecimento em skills
- Configurar LLM Routing (Large/Medium/Small)
- **Entregável:** Skills documentadas e testadas
- **Skills:** deep-research-prompt-creator, skill-creator, write-a-skill, routing-llms
- **Agents:** deep-research-prompt-engineer, skill-engineer

#### Fase 3: Desenvolvimento MVP (1-16 semanas)
- Desenvolvimento orientado a testes (TDD onde couber)
- CI/CD contínuo (commits frequentes, GitHub Actions)
- Dogfooding condicional (usar internamente se aplicável)
- Desenvolvimento iterativo baseado no PRD e SDD
- Construir interface frontend (Next.js)
- Construir automações (Python / n8n)
- MVP funcional em `/executions`
- **Entregável:** MVP funcional cobrindo funcionalidades Must have
- **Skills:** test-driven-development, cicd-pipeline-github-actions, frontend-design, n8n-automation-builder, subagent-driven-development, verification-before-completion
- **Agents:** code-reviewer

#### Fase 4: QA & Validação (3-7 dias)
- Teste de estresse com IA (carga, edge cases, race conditions)
- Simulações de uso manual humana
- QA AI: Evals, testes e validações (LLM-as-Judge)
- Verificação cruzada com modelo alternativo (cross-model)
- Ajustes e correções pós-QA
- **Entregáveis:** Relatórios de estresse, QA, cross-model; bugs corrigidos
- **Skills:** ai-stress-testing, ai-evals, cross-model-verification, systematic-debugging, qa

#### 🚪 Gate 2: MVP
- Teste de aceitação funcional pelo Campeão (Product Owner)
- Validação contra baseline de diagnóstico (métrica definida na Fase 0)

#### Fase 5: Segurança, Deploy & Onboarding (3-5 dias)
- Review de segurança cibernética (vulnerabilidades, OWASP Top 10)
- Ajustar políticas de segurança (CORS, rate limiting, HTTPS, HSTS, CSP)
- Gerar SBOM final
- Criar repositório GitHub (privado, secrets, commit)
- Configurar pipeline CI/CD (GitHub Actions + Easypanel auto-deploy)
- Deploy Easypanel + Hostinger (DNS, SSL, triggers)
- Configurar observabilidade (logs, tracing, alertas, health check)
- Treinamento do cliente (onboarding)
- **Entregáveis:** Sistema em produção, SBOM final, cliente treinado
- **Skills:** security-audit-lgpd, cicd-pipeline-github-actions, easypanel-deploy, hostinger-dns, observabilidade-stack-atomica, client-onboarding-training

#### 🚪 Gate 3: Entrega Final
- Sign-off final do projeto pelo Decisor (CEO/CFO)
- Validação final de segurança pelo Guardião (CISO)
- Entrega de documentação completa (README, PRD, SBOM, Arquitetura, Compliance)

#### Fase 6: Retrospectiva & Melhoria Contínua (2-3 dias)
- Retrospectiva interna documentada (3 sócios)
- Skills reutilizáveis → adicionar à biblioteca Atômica
- Atualizar este processo com lições aprendidas (self-improving)
- Context engineering / token maxing review
- Wrap-up do projeto
- **Skills:** grill-me, brainstorming, skill-creator, context-engineering-2025, handoff

### 5.4 Critérios de Aceitação por Gate

| Gate | Quem aprova | Critério |
|------|------------|----------|
| Gate -1 | Engagement Lead | Reunião de diagnóstico agendada |
| Gate 0 | Decisor | Escopo, prazo e investimento aprovados |
| Gate 1 | Guardião | Stack, arquitetura e compliance aprovados |
| Gate 2 | Campeão | MVP funcional validado contra baseline |
| Gate 3 | Decisor + Guardião | Projeto aceito, documentação entregue |

---

## 6. Comportamento Esperado do Agente

### 6.1 Regras de Ouro (Inegociáveis)

| # | Regra | Motivo |
|---|-------|--------|
| R1 | Nunca expor chaves secretas nas respostas | Segurança |
| R2 | Nunca logar e-mails, dados de pagamento ou PII | Privacidade / LGPD |
| R3 | Nunca hardcodar segredos — sempre ler de `.env` | Portabilidade |
| R4 | Nunca modificar chaves existentes no `.env` sem ordem explícita | Integridade |
| R5 | Sempre ler a diretiva relevante antes de executar | Conformidade |
| R6 | Se falhar, seguir o protocolo de autocorreção antes de escalar | Autonomia |

### 6.2 Ciclo de Execução Padrão

1. Ler a diretiva relevante em `directives/`
2. Identificar ou criar o script em `executions/`
3. Executar, capturar logs, validar resultado
4. Em caso de falha: Protocolo de Autocorreção (§6.3)
5. Registrar alterações no changelog

### 6.3 Protocolo de Autocorreção

1. **Ler** a mensagem de erro completa
2. **Diagnosticar** a causa raiz (não o sintoma)
3. **Corrigir** e testar novamente
4. **Se a lógica de negócio mudou**: atualizar a diretiva (`directives/`) **antes** do código

### 6.4 Definition of Done

Uma tarefa só está concluída quando:

1. O código/script executa sem erros
2. Variáveis sensíveis estão no `.env` (nunca no código)
3. Arquivos novos seguem a convenção do projeto
4. Mudanças foram registradas em `directives/updates.md` ou no changelog da diretiva específica

---

## 7. Requisitos Não-Funcionais

| Requisito | Especificação |
|-----------|--------------|
| **Portabilidade** | Código agnóstico de SO (usar `pathlib`, nunca hardcodar `\` ou `/`) |
| **Deploy** | Todo sistema deve rodar via Docker Compose em qualquer VPS |
| **Configuração** | `.env` como fonte única de config por ambiente (dev, staging, prod) |
| **Rastreabilidade** | Toda alteração importante registrada em changelog com data e motivo |
| **Segurança** | Tokens e secrets nunca versionados; `.env` no `.gitignore` |
| **Contexto do agente** | Usar sub-agentes para tarefas paralelas; manter uso de contexto < 50% |

---

## 8. Roadmap e Evolução

| Fase | Entregável | Status |
|------|-----------|--------|
| v1.0 | Estrutura base, framework DOE, manifesto do agente | ✅ Atual |
| v1.1 | Skills especializadas, comandos customizados | 🔜 Planejado |
| v1.2 | Templates de PRD e arquitetura preenchíveis | 🔜 Planejado |

---

## 9. Processo de Onboarding de Novos Projetos

Todo novo projeto segue o processo completo documentado em `directives/atomica-processos.csv` (resumido na §5). O setup técnico inicial segue o fluxo abaixo:

1. Clonar este repositório como template
2. Atualizar `REPOSITORY_NAME` no `.env`
3. Seguir **Fase 1** do processo: importar contexto, criar PRD Agentive, definir arquitetura
4. Preencher `directives/PRD.md` com o escopo do novo projeto
5. Preencher `directives/architecture.md` com a arquitetura específica
6. Ajustar `directives/brand_voice.md` se aplicável
7. Personalizar `.agents/agents.md` conforme necessidade
8. Criar skills em `.agents/skills/` conforme **Fase 2**
9. Desenvolver seguindo **Fase 3** (MVP) e validar na **Fase 4** (QA)
10. Deploy e onboarding seguindo **Fase 5**

---

*Última atualização: 2026-06-12 | Autor: Agente Qwen Code + Pedro (Atômica)*
