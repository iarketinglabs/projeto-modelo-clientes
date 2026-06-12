# Sobre o Template — Framework DOE & Processo Atômica

> Documentação do **projeto-modelo-clientes** como produto interno da Atômica.
> Isto NÃO é documentação de projeto de cliente — é a fundação que todo projeto herda.

---

## 1. O que é o Projeto Modelo

O **projeto-modelo-clientes** é o template/starter kit canônico da Atômica para inicialização de novos projetos de cliente. Ele padroniza:

- Estrutura de diretórios
- Framework DOE (Diretivas, Orquestração, Execução)
- Comportamento de agentes de IA como executores autônomos
- Stack tecnológica default
- Processo de projeto (6 fases + 7 gates)

---

## 2. Framework DOE

O projeto adota o framework **DOE** que separa responsabilidades em três camadas deterministicamente isoladas:

| Camada | Local | Responsabilidade | Restrição |
|--------|-------|------------------|-----------|
| **Diretivas** | `directives/` | SOPs, regras de negócio, PRDs em Markdown | **Zero código executável** |
| **Orquestração** | Agente + `.agents/` | Roteamento, decisão tática, escolha de ferramentas e skills | Sempre lê a diretiva antes de executar |
| **Execução** | `executions/` | Scripts atômicos e determinísticos (Python, JS, Shell) | **Uma única responsabilidade** por script |

### Por que três camadas?

LLMs são probabilísticos; a lógica de negócio não pode ser. O DOE garante que:

- **Diretivas** documentam o "o quê" e o "porquê"
- **Execuções** implementam o "como" de forma determinística e testável
- **Orquestração** (o agente) apenas conecta as duas pontas

---

## 3. Estrutura de Diretórios

```
projeto-modelo-clientes/
├── orientacao/              # Documentação do template (você está aqui)
│   ├── README.md
│   ├── sobre-o-template.md  # Este arquivo
│   └── guia-onboarding.md   # Passo a passo para novos projetos
├── .agents/                 # Configuração dos agentes de IA
│   ├── agents.md            # ★ Manifesto de operação (system prompt)
│   ├── agents/              # Sub-agentes (prd-engineer, code-reviewer, etc.)
│   ├── commands/            # Comandos customizados
│   ├── hooks/               # Hooks de ciclo de vida
│   ├── rules/               # Regras aprendidas
│   └── skills/              # Skills especializadas (herdadas pelo cliente)
├── directives/              # ★ Placeholders — substituir pelo conteúdo do cliente
│   ├── PRD.md               # ⚠️ Preencher com PRD do projeto do cliente
│   ├── architecture.md      # ⚠️ Preencher com arquitetura do cliente
│   ├── brand_voice.md       # ⚠️ Preencher com voz da marca do cliente
│   └── atomica-processos.csv # Processo de referência (não alterar)
├── executions/              # Onde o código do cliente vai morar
│   ├── app/                 # Aplicação (Next.js)
│   ├── scripts/             # Scripts Python/JS
│   └── src/                 # Código fonte
├── tmp/                     # Arquivos temporários
├── .env                     # Secrets (NÃO versionado)
├── .gitignore
└── README.md
```

---

## 4. Stack Tecnológica Default

Se o cliente não tiver stack própria, estas são as escolhas canônicas:

| Camada | Tecnologia |
|--------|-----------|
| Automação / Scripts | **Python 3.11+** |
| Web / APIs | **Next.js + Tailwind CSS** |
| Banco de dados | **PostgreSQL** (prod) / SQLite (proto) |
| Infraestrutura | **Docker + Docker Compose** |
| Deploy | **Easypanel + Hostinger** |
| CI/CD | **GitHub Actions** |
| Design | Minimalista, Apple-like |

---

## 5. Processo Atômica de Projetos (6 Fases + 7 Gates)

O processo completo está documentado em `directives/atomica-processos.csv`.

```
🚪 Gate -1 → Fase 0 → 🚪 Gate 0 → Fase 1 → 🚪 Gate 1 → Fase 2
Diagnóstico   (2-5d)    Kickoff     (3-7d)    Arq.        Skills

Fase 3 → Fase 4 → 🚪 Gate 2 → Fase 5 → 🚪 Gate 3 → Fase 6
MVP      QA        Aceitação   Deploy     Entrega    Retrosp.
```

### Papéis

| Papel | Lado | Função |
|-------|------|--------|
| **Engagement Lead** | Atômica | Relacionamento, diagnóstico, alinhamento |
| **Tech Lead** | Atômica | Arquitetura, código, stack, segurança |
| **Delivery Manager** | Atômica | Cronograma, riscos, prazos |
| **Decisor** | Cliente | CEO/CFO — aprova gates e escopo |
| **Campeão** | Cliente | Product Owner — valida requisitos |
| **Guardião** | Cliente | CISO/TI — aprova segurança |

---

## 6. Regras de Ouro do Agente

| # | Regra |
|---|-------|
| R1 | Nunca expor chaves secretas nas respostas |
| R2 | Nunca logar e-mails, dados de pagamento ou PII |
| R3 | Nunca hardcodar segredos — sempre ler de `.env` |
| R4 | Nunca modificar chaves existentes no `.env` sem ordem explícita |
| R5 | Sempre ler a diretiva relevante antes de executar |
| R6 | Se falhar, seguir o protocolo de autocorreção antes de escalar |

### Protocolo de Autocorreção

1. **Ler** a mensagem de erro completa
2. **Diagnosticar** a causa raiz (não o sintoma)
3. **Corrigir** e testar novamente
4. **Se a lógica de negócio mudou**: atualizar a diretiva **antes** do código

### Definition of Done

1. Código/script executa sem erros
2. Variáveis sensíveis estão no `.env` (nunca no código)
3. Arquivos novos seguem a convenção do projeto
4. Mudanças registradas no changelog

---

## 7. Requisitos Não-Funcionais Baseline

| Requisito | Especificação |
|-----------|--------------|
| **Portabilidade** | Código agnóstico de SO (`pathlib`, sem hardcode de paths) |
| **Deploy** | Docker Compose em qualquer VPS |
| **Configuração** | `.env` como fonte única por ambiente |
| **Rastreabilidade** | Changelog com data e motivo |
| **Segurança** | Tokens nunca versionados; `.env` no `.gitignore` |
| **Contexto do agente** | Sub-agentes para tarefas paralelas; contexto < 50% |

---

*Última atualização: 2026-06-12 | Atômica*
