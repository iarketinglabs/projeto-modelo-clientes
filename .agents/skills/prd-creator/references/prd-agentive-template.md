# Template de PRD Final (Agentive PRD)

Use este template obrigatoriamente ao gerar o PRD. O documento deve ser em Markdown, no idioma do usuário, conciso mas completo.

```markdown
# PRD: [Nome do Produto/Feature]

## 1. Contexto e Visão

### 1.1 Problema
[Descrição do problema real, validado. Não é a solução.]

### 1.2 Solução Proposta
[Descrição de alto nível do produto/feature]

### 1.3 Personas
- **Persona 1: [Nome]** — [Cargo/perfil], [contexto], [objetivo com o sistema]
- **Persona 2: [Nome]** — [...]

### 1.4 Stakeholders e Papéis
| Nome/Papel | Responsabilidade | Poder de Decisão |
|---|---|---|
| [PO/Analista] | [...] | [Alta/Média/Baixa] |

### 1.5 Objetivos de Negócio e KPIs
| Objetivo | Métrica Atual | Meta | Prazo |
|---|---|---|---|
| [...] | [...] | [...] | [...] |

---

## 2. Escopo

### 2.1 In-Scope (O que será entregue)
- [Feature/Funcionalidade 1]
- [Feature/Funcionalidade 2]

### 2.2 Out-of-Scope (O que NÃO será entregue nesta versão)
- [Item explicitamente excluído]

### 2.3 Premissas e Dependências
- [Premissa 1: se falsa, o projeto muda]
- [Dependência 1: bloqueia X se não estiver pronta]

---

## 3. Funcionalidades e Requisitos Funcionais

### 3.1 [Feature ID-001: Nome da Feature]

**Descrição:** [O que esta feature faz em uma frase]

**User Story:**
> Como [persona], quero [ação] para que [benefício].

**Fluxo Principal:**
1. [Passo 1: usuário faz X]
2. [Passo 2: sistema responde Y]
3. [...]

**Regras de Negócio:**
- [RN-001]: [Regra estruturada: SE condição ENTÃO ação SENÃO ação alternativa]
- [RN-002]: [...]

**Critérios de Aceitação (BDD):**

**Cenário 1: [Caminho feliz]**
- Given [pré-condição]
- And [pré-condição adicional, se houver]
- When [ação do usuário/sistema]
- Then [resultado esperado 1]
- And [resultado esperado 2]

**Cenário 2: [Erro/Edge case]**
- Given [pré-condição]
- When [ação que dispara erro]
- Then [comportamento esperado: mensagem, estado, log]

**Cenário 3: [Outro edge case]**
- [...]

**Dependências:** [Depende de ID-XXX ou API Y]
**Prioridade:** [Must/Should/Could]
**Estimativa (se houver):** [Story Points ou tamanho]

### 3.2 [Feature ID-002: Nome da Feature]
[Mesma estrutura]

---

## 4. Requisitos Não-Funcionais (RNF)

| ID | Categoria | Requisito | Métrica/Meta |
|---|---|---|---|
| RNF-001 | Performance | Tempo de resposta da API | < 200ms para 95% das requisições sob carga normal (1.000 req/s) |
| RNF-002 | Disponibilidade | Uptime do sistema | 99.9% exceto janelas de manutenção agendadas |
| RNF-003 | Segurança | Criptografia de dados | AES-256 em repouso, TLS 1.3 em trânsito |
| RNF-004 | Escalabilidade | Capacidade de usuários | Suportar 10.000 usuários simultâneos com auto-scaling |
| RNF-005 | Usabilidade | Acessibilidade | WCAG 2.1 nível AA |
| [...] | [...] | [...] | [...] |

---

## 5. Regras de Negócio Globais

- [RN-GLOBAL-001]: [Regra que se aplica a múltiplas features]
- [RN-GLOBAL-002]: [...]

---

## 6. Edge Cases e Tratamento de Erros Globais

| Cenário | Condição | Comportamento Esperado |
|---|---|---|
| [Nome do cenário] | [Quando ocorre] | [O que o sistema deve fazer] |
| API externa indisponível | Timeout > 5s ou status 5xx | Retry com exponential backoff (máx 3 tentativas); fallback para cache; notificar admin |
| Sessão expirada | JWT inválido ou expirado | Redirecionar para login com mensagem; preservar rascunho em localStorage se aplicável |
| [...] | [...] | [...] |

---

## 7. Restrições Técnicas

- **Stack Obrigatória:** [tecnologias que DEVEM ser usadas]
- **Stack Proibida:** [tecnologias que NÃO podem ser usadas]
- **Infraestrutura:** [AWS/Azure/GCP/on-premise, região, containers]
- **Padrões:** [REST/GraphQL/gRPC, convenções de código, design system]
- **Compliance:** [LGPD, GDPR, PCI DSS, etc.]

---

## 8. Integrações e Dependências

| Sistema/API | Tipo | Dados Trocados | Protocolo | Critério de Falha |
|---|---|---|---|---|
| [Nome] | [Interna/Externa] | [Entrada/Saída] | [REST/SOAP/Queue] | [Comportamento se falhar] |

---

## 9. Priorização

### 9.1 Framework Usado
[MoSCoW / RICE / WSJF]

### 9.2 Matriz de Priorização
| ID | Feature | Categoria/Score | Justificativa |
|---|---|---|---|
| ID-001 | [...] | Must / RICE 120 | [...] |
| ID-002 | [...] | Should / RICE 80 | [...] |

### 9.3 MVP (Mínimo Viável)
[Lista das features Must que compõem a primeira entrega de valor]

---

## 10. Métricas de Sucesso e Definition of Done

### 10.1 Métricas de Negócio
| Métrica | Baseline | Meta | Frequência de Medição |
|---|---|---|---|
| [...] | [...] | [...] | [...] |

### 10.2 Métricas Técnicas
| Métrica | Meta |
|---|---|
| Cobertura de testes unitários | > 80% |
| Tempo médio de resposta (p95) | < 200ms |
| Taxa de erro em produção | < 0.1% |

### 10.3 Definition of Done (DoD)
- [ ] Código revisado por peer
- [ ] Testes unitários passando (cobertura > 80%)
- [ ] Testes de integração passando
- [ ] Testes de aceitação (BDD) passando
- [ ] Documentação técnica atualizada
- [ ] Deploy em ambiente de staging validado
- [ ] Feature flags configuradas (se aplicável)

---

## 11. Glossário de Domínio

| Termo | Definição | Sinônimos a Evitar |
|---|---|---|
| [Termo do domínio] | [Significado preciso neste contexto] | [Palavras que podem confundir a IA] |
| [Ex: Pedido] | [Solicitação de compra feita pelo cliente final] | [Ordem, Requisição, Ordem de Serviço] |

---

## 12. Apêndices

### 12.1 Notas Técnicas para o Agente de IA
- [Instruções específicas sobre padrões de código, arquitetura preferida, ou decisões já tomadas]
- [Links para documentação de APIs, design system, ou repos de referência]

### 12.2 Riscos e Mitigações
| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| [...] | [Alta/Média/Baixa] | [Alto/Médio/Baixo] | [...] |

### 12.3 Histórico de Versões
| Versão | Data | Autor | Alterações |
|---|---|---|---|
| 0.1 | [data] | [autor] | [escopo inicial] |
```

## Notas sobre Formato Final

- O PRD deve ser salvo como arquivo `.md` (Markdown).
- Se o projeto tiver múltiplos módulos grandes (> 5 features complexas), considere gerar um PRD mestre + SPEC.md individuais por módulo.
- O PRD mestre deve conter visão, escopo, priorização, RNFs e glossário.
- Cada SPEC.md de módulo deve conter contexto, comportamentos BDD, edge cases e restrições daquele módulo.
- Isso mantém cada documento abaixo de 300–500 linhas, respeitando os limites de contexto das LLMs.
