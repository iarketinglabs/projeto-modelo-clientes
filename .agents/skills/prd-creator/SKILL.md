---
name: prd-creator
description: Cria Product Requirements Documents (PRDs) completos e prontos para consumo por agentes de IA de código. Use SEMPRE que o usuário pedir para criar um PRD, documentar requisitos de produto, especificar funcionalidades para desenvolvimento, preparar specs para projeto, ou estruturar um produto antes de codar. Atua através de entrevista estruturada em múltiplas levas até mitigar todas as lacunas de informação, gerando um PRD no padrão Agentive PRD otimizado para IA. Use também quando o usuário mencionar "vibe coding", "spec-driven development", "especificar antes de codar", ou "documentar para IA desenvolver".
---

# PRD Creator

Skill para criação de Product Requirements Documents (PRDs) de altíssima qualidade, otimizados para consumo por agentes de IA especializados em código (Claude Code, Cursor, GitHub Copilot, etc.).

A premissa central: **um PRD incompleto ou ambíguo gera código que "parece certo mas não funciona"**. Portanto, esta skill NUNCA gera um PRD na primeira interação. Ela conduz uma entrevista estruturada em múltiplas levas até que todas as lacunas críticas sejam preenchidas.

## Princípios Fundamentais

1. **Elicitação antes de Documentação:** Não documente o que não foi devidamente elicitado. Use as técnicas dos Cinco Porquês, JTBD e análise de stakeholders para chegar à raiz do problema.
2. **Múltiplas Levas de Perguntas:** Uma única rodada de perguntas nunca é suficiente. Cada resposta do usuário gera novas questões de clarificação.
3. **Zero Ambiguidade:** Termos como "rápido", "fácil", "intuitivo", "escalável" são proibidos no PRD final sem quantificação numérica.
4. **PRD como Contrato para IA:** O documento final deve ser consumível por uma LLM. Isso significa contexto explícito, comportamentos em BDD, edge cases isolados, restrições imperativas e glossário de domínio.
5. **Só Gere Quando Estiver Pronto:** O PRD só é gerado quando o checklist de completude for 100% atendido.

---

## Processo de Entrevista em Múltiplas Levas

O processo segue obrigatoriamente as levas abaixo. **Não pule levas**, mesmo que o usuário ache que já respondeu tudo. Cada leva valida e aprofunda a anterior.

### Leva 1 — Contexto, Problema e Stakeholders (O Porquê)

Objetivo: entender O PORQUÊ do produto existir, PARA QUEM, e qual problema real resolve.

Perguntas obrigatórias (faça todas de forma conversacional, não como formulário):

- **Qual é o problema real que este produto resolve?** (Use a Técnica dos Cinco Porquês se a resposta soar como uma solução — ex: "quero um dashboard" → por quê? → "preciso acompanhar métricas" → por quê? etc.)
- **Quem são os usuários primários?** Descreva as personas: cargo, contexto de trabalho, nível de familiaridade com tecnologia, frequência de uso.
- **Quem são os stakeholders decisores?** Quem aprova, quem paga, quem pode bloquear?
- **O que acontece hoje sem este produto?** Como o problema é resolvido atualmente? Quais as limitações dessa solução atual?
- **Qual seria o impacto mensurável de sucesso?** (KPIs, métricas de negócio — evite "melhorar a experiência"; exija números ou indicadores concretos)
- **Este produto é um MVP, uma evolução de produto existente, ou uma migração?** Contexto histórico muda completamente o escopo.
- **Existe algum prazo ou evento de mercado que impõe urgência?**

**Critério de passagem:** Você consegue explicar para um terceiro, em uma frase, qual problema este produto resolve e para quem.

**Referência detalhada:** Leia `references/interview-checklist.md` para o checklist completo desta leva.

### Leva 2 — Escopo, Fronteira do Sistema e Exclusões (O Quê)

Objetivo: delimitar com precisão o que está DENTRO e o que está FORA do escopo. Previne scope creep.

Perguntas obrigatórias:

- **Liste as funcionalidades principais que você imagina.** (Capture como bullet points inicial; não detalhe ainda)
- **O que está explicitamente FORA do escopo desta primeira versão?** (Force respostas concretas. "Não sabemos ainda" não é aceitável — transforme em hipóteses)
- **Este produto precisa integrar com sistemas, APIs ou bancos de dados existentes?** Quais? Com que nível de acesso?
- **Há dados que precisam ser migrados de sistemas legados?**
- **O produto precisa funcionar em múltiplas plataformas?** (Web, mobile iOS/Android nativo, desktop, PWA, etc.)
- **Há requisitos regulatórios ou de compliance?** (LGPD, GDPR, PCI DSS, HIPAA, SOX, etc.)
- **Existe um orçamento máximo ou restrição de licenciamento?**

**Critério de passagem:** Você consegue desenhar uma fronteira clara do sistema: o que ele faz, o que ele NÃO faz, e com o que se conecta.

### Leva 3 — Fluxos de Usuário, Funcionalidades e Comportamentos (O Como do Usuário)

Objetivo: detalhar CADA funcionalidade principal com fluxos de usuário, regras de negócio e critérios de aceitação.

Para cada funcionalidade listada na Leva 2, faça:

- **Qual é a jornada do usuário para completar esta tarefa?** Descreva passo a passo, do início ao fim.
- **Quais são as regras de negócio que governam este fluxo?** (Ex: "clientes com score < 600 não podem solicitar crédito")
- **Quais são os dados de entrada, processamento e saída?**
- **Quem pode acessar/executar esta funcionalidade?** (Autorização, perfis, papéis)
- **O que acontece se o usuário abandonar o fluxo no meio?**
- **Existe notificação, email, SMS ou webhook disparado?** Quando, para quem, com qual conteúdo?
- **Esta funcionalidade depende de outra estar pronta primeiro?**

**Técnica de Story Mapping:** Organize funcionalidades na ordem da jornada do usuário (eixo horizontal) e por profundidade/prioridade (eixo vertical). Isso revela lacunas de fluxo.

**Critério de passagem:** Cada funcionalidade principal tem um fluxo de usuário mapeado, regras de negócio identificadas e dependências explicitadas.

### Leva 4 — Edge Cases, Erros, Estados Extremos e Segurança (O Que Pode Dar Errado)

Objetivo: mitigar o viés do happy path. LLMs tendem a gerar código apenas para o caminho feliz se não instruídas explicitamente.

Perguntas obrigatórias (para cada funcionalidade ou de forma global):

- **Quais são os principais cenários de erro que o sistema deve tratar?** (Dados inválidos, falha de rede, timeout, serviço externo indisponível, permissão negada)
- **O que o sistema deve fazer quando uma API externa falha?** (Retry? Circuit breaker? Fallback? Notificação?)
- **Como o sistema deve se comportar com dados em volume extremo?** (Upload de 10 mil registros, lista com 1 milhão de itens)
- **Como o sistema deve lidar com ações simultâneas do mesmo usuário?** (Duplo clique, submit duplicado, race conditions)
- **Quais são os limites de entrada de dados?** (Tamanho máximo de arquivo, caracteres por campo, formatos aceitos)
- **O que acontece com dados em rascunho ou não salvos se a sessão expirar?**
- **Existe necessidade de auditoria ou log de ações para compliance?**
- **Quais são os cenários de segurança a considerar?** (XSS, SQL injection, rate limiting, brute force, leak de dados sensíveis)

**Referência detalhada:** Leia `references/edge-case-catalog.md` para catálogo exaustivo de edge cases por tipo de sistema. Use-o como inspiração durante a entrevista.

**Critério de passagem:** Para cada funcionalidade principal, você identificou pelo menos 2 cenários de erro/exceção e o comportamento esperado do sistema.

### Leva 5 — Requisitos Não-Funcionais, Restrições Técnicas e Arquitetura (Como o Sistema Deve Operar)

Objetivo: especificar atributos de qualidade mensuráveis e restrições que definem o espaço de solução.

Perguntas obrigatórias:

- **Qual stack tecnológica é obrigatória, preferida ou proibida?** (Linguagens, frameworks, bancos de dados, cloud provider)
- **Quantos usuários simultâneos o sistema deve suportar?** (Carga normal e pico)
- **Qual é o tempo máximo de resposta aceitável para as operações críticas?**
- **Qual é a meta de disponibilidade (uptime)?** (Ex: 99.9%, com janela de manutenção?)
- **O sistema precisa operar offline ou tem tolerância a falhas de rede?**
- **Há requisitos de backup, recuperação de desastre ou RPO/RTO definidos?**
- **O sistema precisa ser multi-idioma, multi-moeda ou multi-tenant?**
- **Existem padrões de código, arquitetura ou design system que devem ser seguidos?**
- **Há bibliotecas, SDKs ou serviços de terceiros que devem ser usados ou evitados?**
- **O sistema precisa seguir algum padrão de acessibilidade?** (WCAG 2.1 nível AA, etc.)

**Referência detalhada:** Leia `references/rnf-metric-guide.md` para converter qualquer RNF subjetivo em métrica quantificável.

**Critério de passagem:** Todos os RNFs possuem valores numéricos, métricas ou instruções imperativas. Nenhum RNF é subjetivo.

### Leva 6 — Priorização, Métricas de Sucesso e Definição de Pronto (Quando Sabemos que Deu Certo)

Objetivo: definir como o sucesso será medido e o que significa "terminado".

Perguntas obrigatórias:

- **Como priorizaríamos as funcionalidades se metade do time fosse cortado?** (Force priorização real — use MoSCoW, RICE ou WSJF)
- **Qual é o MVP mínimo que já entrega valor mensurável?** (Walking skeleton)
- **Quais métricas técnicas indicam saúde do sistema?** (Latência, taxa de erro, cobertura de testes)
- **Quais métricas de negócio indicam sucesso do produto?** (Adoção, conversão, retenção, NPS)
- **Qual é a Definition of Done?** (Code review, testes unitários, testes de integração, documentação, deploy em staging)
- **Existem critérios de aceitação globais que se aplicam a TODAS as funcionalidades?**
- **Há necessidade de testes A/B, feature flags ou rollout gradual?**

**Critério de passagem:** Você consegue ranquear as funcionalidades por valor/urgência e definir o que significa "pronto" para este projeto.

---

## Checklist de Completude do PRD

Antes de gerar o PRD final, verifique se TODOS os itens abaixo estão preenchidos. Se algum estiver faltando ou incompleto, volte às levas correspondentes.

- [ ] Problema de negócio claramente definido (não é uma solução mascarada)
- [ ] Personas de usuário descritas com contexto real
- [ ] Escopo in-scope e out-of-scope explicitamente listados
- [ ] Cada funcionalidade principal tem fluxo de usuário mapeado
- [ ] Regras de negócio documentadas sem ambiguidade (tabelas de decisão quando aplicável)
- [ ] Critérios de aceitação BDD (Given/When/Then) para cada funcionalidade
- [ ] Edge cases e cenários de erro identificados com comportamentos esperados
- [ ] Requisitos não-funcionais com métricas quantificáveis
- [ ] Restrições técnicas listadas (stack obrigatória, proibições, compliance)
- [ ] Dependências e integrações mapeadas
- [ ] Priorização das funcionalidades (MoSCoW, RICE ou WSJF)
- [ ] Métricas de sucesso e KPIs definidos
- [ ] Definition of Done estabelecida
- [ ] Glossário de termos do domínio (evita que a IA interprete "pedido" como "ordem" ou "requisição")

**Referência detalhada:** Leia `references/interview-checklist.md` para o checklist expandido por leva.

---

## Geração do PRD Final

Quando o checklist estiver 100%, gere o PRD usando obrigatoriamente o template em `references/prd-agentive-template.md`.

O documento deve ser escrito em Markdown, no idioma do usuário, conciso mas completo.

### Após Gerar o PRD

1. Ofereça-se para **revisar e ajustar** qualquer seção.
2. Pergunte se há **novos edge cases** que não foram cobertos.
3. **Valide o PRD com o script:** Execute `python scripts/validate_prd.py <arquivo_prd.md>` para verificar se o documento gerado atende aos critérios mínimos. Se o script reportar issues, corrija antes de entregar ao usuário.
4. Sugira criar um **CLAUDE.md** ou **AGENTS.md** complementar se o projeto for grande o suficiente para justificar contexto global separado.
5. Ofereça exportar o PRD para um arquivo `.md` no workspace do usuário.

---

## Instruções de Execução para o Agente

### Ao Iniciar
1. Apresente-se como especialista em criação de PRDs para desenvolvimento com IA.
2. Explique que o processo leva **múltiplas levas de perguntas** e que isso é intencional para garantir qualidade.
3. Pergunte: **"Me conte, em poucas frases, qual produto ou feature você precisa documentar?"**
4. Capture a resposta e imediatamente identifique ambiguidades ou lacunas para a Leva 1.

### Durante as Levas
- **Nunca faça todas as perguntas de uma vez.** Envie 3–5 perguntas por mensagem, analise as respostas, faça follow-ups de clarificação.
- **Use tabelas de decisão** quando regras de negócio envolverem múltiplas variáveis.
- **Desafie termos vagos.** Se o usuário disser "rápido", pergunte "quanto tempo em segundos?". Se disser "muitos usuários", pergunte "quantos simultâneos?".
- **Faça o usuário priorizar.** Se surgirem mais de 5 features, force a ordenação por valor.
- **Valide com espelhamento:** "Entendi que [resumo]. Está correto?"

### Antes de Gerar o PRD
1. Execute mentalmente o Checklist de Completude.
2. Se houver itens pendentes, comunique claramente: **"Ainda precisamos esclarecer [X] antes de gerar o PRD. Vamos à Leva [N]."**
3. Se o checklist estiver completo, avise: **"Tenho todas as informações necessárias. Vou gerar o PRD agora no formato Agentive PRD."**

---

## Anti-Padrões a Evitar

| Anti-Padrão | Por que é Perigoso | Como Evitar |
|---|---|---|
| **Gerar PRD na primeira interação** | Gera documento incompleto, ambíguo e inútil para IA | Siga obrigatoriamente as 6 levas |
| **Aceitar termos subjetivos** | "Rápido", "fácil", "intuitivo" não são implementáveis | Sempre exija quantificação |
| **Ignorar out-of-scope** | Scope creep silencioso destrói prazos | Documente explicitamente o que NÃO será feito |
| **Esquecer edge cases** | A IA gerará código que quebra em produção | Dedicar Leva 4 inteiramente a erros e estados extremos |
| **RNFs sem métricas** | "O sistema deve ser escalável" não instrui nada | Sempre ligue RNF a um número testável. Use `references/rnf-metric-guide.md` |
| **Mesclar contexto global com especificação** | PRD inchado > 500 linhas perde foco da IA | Contexto global vai em CLAUDE.md/AGENTS.md; PRD fica enxuto |
| **Não definir glossário** | A IA pode interpretar termos do domínio de forma errada | Sempre inclua glossário com sinônimos a evitar |

---

## Exemplo de Interação Completa (Resumido)

**Usuário:** "Preciso de um PRD para um sistema de agendamento de consultas médicas."

**Agente (Leva 1):** "Ótimo. Para criar um PRD completo, vou fazer algumas perguntas em etapas. Vamos começar com o problema real: por que este sistema é necessário? Quem são os usuários principais — médicos, pacientes, recepcionistas? E qual seria o KPI de sucesso — reduzir tempo de espera, diminuir faltas?"

**Usuário:** [responde]

**Agente (Leva 2):** "Entendido. Agora vamos delimitar o escopo. Este sistema precisa integrar com prontuário eletrônico existente? Vai ter pagamento online? E o que fica FORA do escopo inicial — por exemplo, telemedicina, chat com o médico?"

**Usuário:** [responde]

**Agente (Leva 3–6):** [continua com perguntas de aprofundamento]

**Agente (Checklist):** "Verificando completude... Identifiquei que ainda não temos os limites de cancelamento (edge case da Leva 4). Se um paciente cancela com menos de 24h, o que o sistema faz?"

**Usuário:** [responde]

**Agente (Geração):** "Perfeito, checklist 100%. Gerando o PRD no formato Agentive PRD..."

**[Gera o PRD completo usando o template de `references/prd-agentive-template.md`]**

**Agente (Validação):** "Agora vou validar o PRD gerado... Executando script de validação..."

**[Executa `python scripts/validate_prd.py prd.md`]**

**Agente:** "PRD validado com sucesso! Score: 100%. Nenhuma issue encontrada."
