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

## 5. Comportamento Esperado do Agente

### 5.1 Regras de Ouro (Inegociáveis)

| # | Regra | Motivo |
|---|-------|--------|
| R1 | Nunca expor chaves secretas nas respostas | Segurança |
| R2 | Nunca logar e-mails, dados de pagamento ou PII | Privacidade / LGPD |
| R3 | Nunca hardcodar segredos — sempre ler de `.env` | Portabilidade |
| R4 | Nunca modificar chaves existentes no `.env` sem ordem explícita | Integridade |
| R5 | Sempre ler a diretiva relevante antes de executar | Conformidade |
| R6 | Se falhar, seguir o protocolo de autocorreção antes de escalar | Autonomia |

### 5.2 Ciclo de Execução Padrão

1. Ler a diretiva relevante em `directives/`
2. Identificar ou criar o script em `executions/`
3. Executar, capturar logs, validar resultado
4. Em caso de falha: Protocolo de Autocorreção (§5.3)
5. Registrar alterações no changelog

### 5.3 Protocolo de Autocorreção

1. **Ler** a mensagem de erro completa
2. **Diagnosticar** a causa raiz (não o sintoma)
3. **Corrigir** e testar novamente
4. **Se a lógica de negócio mudou**: atualizar a diretiva (`directives/`) **antes** do código

### 5.4 Definition of Done

Uma tarefa só está concluída quando:

1. O código/script executa sem erros
2. Variáveis sensíveis estão no `.env` (nunca no código)
3. Arquivos novos seguem a convenção do projeto
4. Mudanças foram registradas em `directives/updates.md` ou no changelog da diretiva específica

---

## 6. Requisitos Não-Funcionais

| Requisito | Especificação |
|-----------|--------------|
| **Portabilidade** | Código agnóstico de SO (usar `pathlib`, nunca hardcodar `\` ou `/`) |
| **Deploy** | Todo sistema deve rodar via Docker Compose em qualquer VPS |
| **Configuração** | `.env` como fonte única de config por ambiente (dev, staging, prod) |
| **Rastreabilidade** | Toda alteração importante registrada em changelog com data e motivo |
| **Segurança** | Tokens e secrets nunca versionados; `.env` no `.gitignore` |
| **Contexto do agente** | Usar sub-agentes para tarefas paralelas; manter uso de contexto < 50% |

---

## 7. Roadmap e Evolução

| Fase | Entregável | Status |
|------|-----------|--------|
| v1.0 | Estrutura base, framework DOE, manifesto do agente | ✅ Atual |
| v1.1 | Skills especializadas, comandos customizados | 🔜 Planejado |
| v1.2 | Templates de PRD e arquitetura preenchíveis | 🔜 Planejado |

---

## 8. Processo de Onboarding de Novos Projetos

1. Clonar este repositório como template
2. Atualizar `REPOSITORY_NAME` no `.env`
3. Preencher `directives/PRD.md` com o escopo do novo projeto
4. Preencher `directives/architecture.md` com a arquitetura específica
5. Ajustar `directives/brand_voice.md` se aplicável
6. Personalizar `.agents/agents.md` conforme necessidade
7. Criar scripts em `executions/` conforme demandas surgirem
8. Primeiro commit com a estrutura adaptada

---

*Última atualização: 2026-06-12 | Autor: Agente Qwen Code + Pedro (Atômica)*
