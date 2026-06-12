# Guia de Métricas para Requisitos Não-Funcionais

Requisitos não-funcionais subjetivos são inúteis para agentes de IA. Use este guia para transformar qualquer RNF vago em uma especificação mensurável e testável.

**Regra de ouro:** Se não é possível criar um teste finito e econômico para provar que o RNF foi atendido, ele é inadequado.

---

## 1. Performance

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "O sistema deve ser rápido" | "A API de consulta deve responder em menos de 200ms para 95% das requisições sob carga normal de 1.000 req/s" |
| "Carregamento rápido da página" | "Time to Interactive (TTI) < 3s em conexão 4G simulada" |
| "Busca eficiente" | "Resultados de busca retornados em < 500ms para bases de até 10M registros" |
| "Processamento em tempo real" | "Latência p99 < 100ms do evento recebido ao processamento completo" |
| "Baixo consumo de memória" | "Uso de heap < 512MB por instância sob carga de pico" |

**Métricas úteis:**
- Latência (ms): p50, p95, p99
- Throughput (req/s, transações/s)
- Time to First Byte (TTFB)
- First Contentful Paint (FCP) / Largest Contentful Paint (LCP)
- CPU utilization sob carga (%)

---

## 2. Disponibilidade e Confiabilidade

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "O sistema deve estar sempre no ar" | "99.9% de uptime mensurado por Pingdom/DataDog, exceto janelas de manutenção agendadas com 48h de antecedência" |
| "Alta disponibilidade" | "99.99% uptime com failover automático entre 2+ availability zones em < 30s" |
| "O sistema não pode parar" | "RTO (Recovery Time Objective) < 15 minutos; RPO (Recovery Point Objective) < 5 minutos de dados" |
| "Resiliente a falhas" | "Degradação graceful: se o serviço de recomendação cair, a home continua funcionando com conteúdo estático em cache" |

**Métricas úteis:**
- Uptime (%): 99.0%, 99.9%, 99.99%, 99.999%
- MTBF (Mean Time Between Failures)
- MTTR (Mean Time To Recovery)
- RTO / RPO
- Taxa de erro (% de requests 5xx)

---

## 3. Escalabilidade

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "O sistema deve escalar bem" | "Suportar 10.000 usuários simultâneos com latência < 200ms; auto-scaling horizontal ativado quando CPU > 70%" |
| "Suportar crescimento" | "Arquitetura deve suportar 10x de carga sem rewrite arquitetural; testado com load test de 100.000 req/s" |
| "Lidar com picos de tráfego" | "Sustentar 300% de pico durante eventos promocionais com degradação graceful (fila de espera para checkout)" |
| "Banco de dados escalável" | "Particionamento automático por tenant_id; sharding configurável; queries < 1s para 100M+ registros" |

**Métricas úteis:**
- Usuários simultâneos suportados
- Requisições por segundo (RPS) de pico sustentável
- Taxa de crescimento esperado (% mês a mês)
- Limite de registros por tabela/coleção antes de partição

---

## 4. Segurança

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "O sistema deve ser seguro" | "Dados em repouso criptografados com AES-256; dados em trânsito com TLS 1.3; OWASP Top 10 mitigados" |
| "Proteger dados dos usuários" | "Conformidade LGPD/GDPR: direito ao esqueço implementado (exclusão em < 30 dias); consentimento auditável" |
| "Prevenir acessos não autorizados" | "RBAC com 4 níveis de permissão; MFA obrigatório para admins; sessão expira após 30 min de inatividade" |
| "Resistir a ataques" | "Rate limiting: 100 req/min por IP; proteção contra brute force: bloqueio após 5 tentativas falhas" |
| "Senhas seguras" | "Hash Argon2id; mínimo 12 caracteres; complexidade: maiúscula, minúscula, número, símbolo; não reutilizar últimas 5" |

**Métricas úteis:**
- CVSS score máximo aceitável para vulnerabilidades conhecidas
- Tempo de patch de vulnerabilidade crítica (horas)
- Número de controles do OWASP ASVS implementados (nível 1, 2 ou 3)
- Penetration test frequency (a cada 6 meses)

---

## 5. Usabilidade e Acessibilidade

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "Interface intuitiva" | "Taxa de conclusão de tarefa core > 90% em teste de usabilidade com 5 usuários novos sem treinamento" |
| "Fácil de usar" | "Time on task para criar pedido < 2 minutos; número de cliques < 5 do login ao checkout" |
| "Acessível" | "Conformidade WCAG 2.1 nível AA; testado com leitores de tela (NVDA, JAWS); navegação 100% por teclado" |
| "Responsivo" | "Layout funcional em viewports: 320px, 768px, 1024px, 1920px; testado em iOS Safari e Chrome Android" |
| "Baixa curva de aprendizado" | "Usuário consegue completar fluxo core no primeiro acesso sem documentação; NPS > 50" |

**Métricas úteis:**
- System Usability Scale (SUS) score
- Task success rate (%)
- Error rate (%)
- Time on task (segundos)
- Customer Effort Score (CES)
- NPS (Net Promoter Score)

---

## 6. Manutenibilidade

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "Código limpo" | "Cobertura de testes unitários > 80%; complexidade ciclomática < 15 por função; lint sem warnings" |
| "Fácil de manter" | "Documentação de API em OpenAPI 3.0; README com instruções de setup em < 15 min; ADRs para decisões arquiteturais" |
| "Baixa dívida técnica" | "SonarQube: zero vulnerabilidades críticas; code smells < 5 por 1.000 linhas; duplicação < 3%" |
| "Fácil de implantar" | "Pipeline CI/CD: build + test + deploy em staging < 10 min; deploy em produção com zero downtime" |

**Métricas úteis:**
- Cobertura de testes (%)
- Complexidade ciclomática média
- Tempo médio para onboarding de novo dev (dias)
- Lead time para mudança (horas)
- Deployment frequency (por dia/semana)
- Change failure rate (%)

---

## 7. Portabilidade e Compatibilidade

| Subjetivo (Proibido) | Mensurável (Obrigatório) |
|---|---|
| "Funciona em qualquer lugar" | "Suporte a Chrome últimas 2 versões, Firefox últimas 2, Safari últimas 2, Edge última; não suportar IE11" |
| "Multiplataforma" | "Executável em contêineres Docker; compatível com AWS EKS e Azure AKS sem modificação de código" |
| "Funciona offline" | "Service Worker cacheando assets e dados críticos; sincronização automática ao reconectar; indicador de modo offline" |

---

## Checklist de Conversão RNF

Ao documentar um RNF, verifique:

- [ ] O requisito tem um número associado? (latência, %, quantidade, tempo)
- [ ] É possível escrever um teste automatizado que prove se foi atendido?
- [ ] O requisito especifica condições de carga ou contexto? ("sob X usuários", "em condição Y")
- [ ] O requisito diferencia entre normal e pico/degradação?
- [ ] O requisito está atrelado a uma ferramenta de observabilidade? (DataDog, New Relic, Prometheus)
