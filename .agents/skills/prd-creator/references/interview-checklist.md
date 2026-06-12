# Checklist de Entrevista por Leva

Use este checklist durante a entrevista para garantir que nenhum item crítico seja esquecido. **Não pule levas.**

---

## Leva 1 — Contexto, Problema e Stakeholders

- [ ] Problema real validado (não é uma solução mascarada — aplique os Cinco Porquês)
- [ ] Personas primárias descritas (cargo, contexto, familiaridade com tecnologia, frequência de uso)
- [ ] Stakeholders decisores identificados (quem aprova, paga, pode bloquear)
- [ ] Solução atual e suas limitações documentadas
- [ ] KPIs/métricas de sucesso definidos com números ou indicadores concretos
- [ ] Tipo de projeto classificado (MVP / evolução / migração)
- [ ] Prazos ou eventos de mercado que impõem urgência

**Critério de passagem:** Consegue explicar em uma frase qual problema resolve e para quem.

---

## Leva 2 — Escopo, Fronteira e Exclusões

- [ ] Funcionalidades principais listadas em bullet points
- [ ] Itens explicitamente FORA do escopo documentados
- [ ] Integrações com sistemas/APIs/bancos de dados existentes mapeadas
- [ ] Necessidade de migração de dados de sistemas legados avaliada
- [ ] Plataformas alvo definidas (web, iOS nativo, Android nativo, desktop, PWA)
- [ ] Requisitos regulatórios/compliance identificados (LGPD, GDPR, PCI DSS, HIPAA, SOX)
- [ ] Restrições orçamentárias ou de licenciamento documentadas

**Critério de passagem:** Consegue desenhar a fronteira do sistema — o que faz, o que não faz, com o que se conecta.

---

## Leva 3 — Fluxos, Funcionalidades e Comportamentos

Para cada funcionalidade principal:
- [ ] Jornada do usuário mapeada passo a passo (início ao fim)
- [ ] Regras de negócio governando o fluxo documentadas
- [ ] Dados de entrada, processamento e saída definidos
- [ ] Autorização e perfis de acesso especificados
- [ ] Comportamento em caso de abandono do fluxo definido
- [ ] Notificações/emails/SMS/webhooks mapeados (quando, para quem, conteúdo)
- [ ] Dependências entre funcionalidades explicitadas

**Técnica complementar:** Story Mapping aplicada para ordenar a jornada do usuário.

**Critério de passagem:** Cada funcionalidade principal tem fluxo, regras e dependências claras.

---

## Leva 4 — Edge Cases, Erros e Estados Extremos

Para cada funcionalidade (ou globalmente):
- [ ] Cenários de erro principais identificados (dados inválidos, falha de rede, timeout, 5xx, permissão negada)
- [ ] Comportamento em falha de API externa definido (retry, circuit breaker, fallback, notificação)
- [ ] Comportamento com volume extremo de dados (upload em massa, listas gigantes)
- [ ] Tratamento de ações simultâneas do mesmo usuário (duplo clique, submit duplicado, race conditions)
- [ ] Limites de entrada definidos (tamanho de arquivo, caracteres, formatos aceitos)
- [ ] Persistência de dados em rascunho/se não salvos se sessão expirar
- [ ] Necessidade de auditoria/log de ações para compliance avaliada
- [ ] Cenários de segurança considerados (XSS, SQL injection, rate limiting, brute force, leak de dados)

**Critério de passagem:** Pelo menos 2 cenários de erro/exceção por funcionalidade principal com comportamento esperado.

---

## Leva 5 — Requisitos Não-Funcionais, Restrições e Arquitetura

- [ ] Stack tecnológica obrigatória, preferida ou proibida definida
- [ ] Capacidade de usuários simultâneos (normal e pico) quantificada
- [ ] Tempo máximo de resposta para operações críticas especificado
- [ ] Meta de disponibilidade/uptime definida (ex: 99.9%)
- [ ] Tolerância a falhas de rede ou operação offline avaliada
- [ ] Requisitos de backup, DR, RPO/RTO definidos
- [ ] Requisitos de internacionalização (multi-idioma, multi-moeda, multi-tenant)
- [ ] Padrões de código, arquitetura ou design system obrigatórios
- [ ] Bibliotecas/SDKs/serviços de terceiros a usar ou evitar
- [ ] Padrão de acessibilidade exigido (ex: WCAG 2.1 nível AA)

**Critério de passagem:** Todos os RNFs possuem valores numéricos, métricas ou instruções imperativas. Nenhum é subjetivo.

---

## Leva 6 — Priorização, Métricas e Definition of Done

- [ ] Funcionalidades priorizadas com framework estruturado (MoSCoW, RICE ou WSJF)
- [ ] MVP mínimo identificado (walking skeleton que entrega valor mensurável)
- [ ] Métricas técnicas de saúde do sistema definidas
- [ ] Métricas de negócio de sucesso do produto definidas
- [ ] Definition of Done (DoD) estabelecida e acordada
- [ ] Critérios de aceitação globais que se aplicam a todas as funcionalidades
- [ ] Necessidade de testes A/B, feature flags ou rollout gradual avaliada

**Critério de passagem:** Consegue ranquear funcionalidades por valor/urgência e definir o que significa "pronto".

---

## Checklist Global de Completude do PRD

Antes de gerar o PRD final, verifique:

- [ ] Problema de negócio claramente definido (não é solução mascarada)
- [ ] Personas descritas com contexto real
- [ ] Escopo in-scope e out-of-scope explicitados
- [ ] Cada funcionalidade principal tem fluxo de usuário mapeado
- [ ] Regras de negócio documentadas sem ambiguidade (tabelas de decisão quando aplicável)
- [ ] Critérios de aceitação BDD (Given/When/Then) para cada funcionalidade
- [ ] Edge cases e cenários de erro identificados com comportamentos esperados
- [ ] Requisitos não-funcionais com métricas quantificáveis
- [ ] Restrições técnicas listadas (stack obrigatória, proibições, compliance)
- [ ] Dependências e integrações mapeadas
- [ ] Priorização das funcionalidades
- [ ] Métricas de sucesso e KPIs definidos
- [ ] Definition of Done estabelecida
- [ ] Glossário de termos do domínio (evita interpretação errada pela IA)
