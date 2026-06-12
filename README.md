# Projeto Modelo · Atômica

> Template canônico para inicialização de projetos da Atômica.
> Estrutura padronizada, framework DOE e comportamento determinístico de agentes de IA.

---

## O que é isto?

O **Projeto Modelo** é o ponto de partida de todo novo projeto na Atômica. Ele define:

- 📂 **Estrutura de diretórios** consistente entre projetos
- 🧠 **Framework DOE** (Diretivas → Orquestração → Execução)
- 🏭 **Processo Atômica** de 6 fases + 7 gates para execução de projetos
- 🤖 **Manifesto do agente** (`agents.md`) — o system prompt que guia agentes de IA como executores autônomos
- 🔧 **Stack tecnológica default** (Python, Next.js, PostgreSQL, Docker)
- 🔒 **Regras de segurança e qualidade** inegociáveis

---

## Framework DOE

```
┌─────────────────────────────────────────────────────┐
│  DIRECTIVAS (directives/)                            │
│  "O quê e porquê" — SOPs em Markdown                 │
│  Zero código executável                              │
├─────────────────────────────────────────────────────┤
│  ORQUESTRAÇÃO (.agents/ + Agente)                    │
│  "Qual ferramenta e quando" — Roteamento e decisão   │
│  Sempre lê a diretiva antes de executar              │
├─────────────────────────────────────────────────────┤
│  EXECUÇÃO (executions/)                              │
│  "Como" — Scripts atômicos e determinísticos         │
│  Um script = uma responsabilidade                    │
└─────────────────────────────────────────────────────┘
```

LLMs são probabilísticos. A lógica de negócio não pode ser. O DOE isola o determinismo na camada de execução e mantém diretivas como fonte da verdade.

---

## Estrutura do Projeto

```
projeto-modelo/
├── .agents/              # Agentes, comandos, hooks, regras e skills
│   ├── agents.md         # ★ Manifesto de operação do agente
│   ├── settings.json     # Configurações
│   └── mcps.json         # Servidores MCP
├── directives/           # Diretrizes de negócio (SOPs)
│   ├── PRD.md            # Product Requirements Document
│   ├── architecture.md   # Arquitetura do sistema
│   └── brand_voice.md    # Voz e tom da marca
├── executions/           # Scripts executáveis
├── tmp/                  # Arquivos temporários
├── .env                  # Segredos (não versionado)
├── .gitignore
└── README.md
```

---

## Como usar como template

> **Importante:** Todo projeto segue o [Processo Atômica](directives/atomica-processos.csv) completo (6 fases + 7 gates). O checklist abaixo cobre apenas o setup técnico inicial.

### 1. Clone e renomeie

```bash
git clone git@github.com:iarketinglabs/projeto-modelo-clientes.git meu-novo-projeto
cd meu-novo-projeto
rm -rf .git && git init
```

### 2. Configure o `.env`

```env
REPOSITORY_NAME=meu-novo-projeto
GITHUB_OWNER=iarketinglabs
GITHUB_TOKEN_REPO_PROJ=ghp_...
```

### 3. Preencha as diretivas

| Arquivo | O que preencher |
|---------|-----------------|
| `directives/PRD.md` | Escopo, requisitos e stack do novo projeto |
| `directives/architecture.md` | Diagrama de arquitetura, serviços, integrações |
| `directives/brand_voice.md` | Tom de voz, persona, diretrizes de copy (se aplicável) |

### 4. Adapte o agente

Ajuste `.agents/agents.md` conforme as necessidades específicas do projeto (regras de negócio, gotchas, stack diferente da default).

### 5. Commit inicial

```bash
git add .
git commit -m "feat: inicialização do projeto a partir do projeto-modelo"
```

---

## Stack Default

| Camada | Padrão |
|--------|--------|
| Automação / Scripts | **Python 3.11+** |
| Web / APIs | **Next.js + Tailwind CSS** |
| Banco de dados | **PostgreSQL** (prod) / SQLite (proto) |
| Infraestrutura | **Docker + Docker Compose** |
| Design | Minimalista, Apple-like |

> Se o projeto exigir stack diferente, documentar em `directives/architecture.md`.

---

## Regras de Ouro

- 🔐 **Nunca** exponha chaves secretas no código ou no chat
- 📄 **Sempre** leia a diretiva antes de executar
- 🐛 **Se falhar**, autocorrija-se antes de pedir ajuda
- 📝 **Toda alteração** importante vai no changelog
- 🧹 **Arquivos temporários** em `tmp/` — apague após o uso

---

## Links rápidos

- [Processo Atômica (CSV)](directives/atomica-processos.csv)
- [Manifesto do Agente](.agents/agents.md)
- [PRD completo](directives/PRD.md)
- [Arquitetura](directives/architecture.md)
- [Brand Voice](directives/brand_voice.md)

---

## Atômica

Automação de fluxos de trabalho, geração de conteúdo, integrações de API e desenvolvimento de ferramentas internas — operado por agentes de IA com autonomia sênior.

---

*Última atualização: 2026-06-12*
