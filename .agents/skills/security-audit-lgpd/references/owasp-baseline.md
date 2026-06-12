# Baseline OWASP e segurança técnica por camada

## Frameworks de referência

Combine estes frameworks para cobrir o espaço entre obrigação jurídica, desenho seguro, supply chain, logging, risco de IA e governança operacional:

- **OWASP Top 10 2025**: Broken Access Control, Security Misconfiguration, Software Supply Chain Failures, Cryptographic Failures, Injection, Insecure Design, Authentication Failures, Software or Data Integrity Failures, Security Logging and Alerting Failures, Mishandling of Exceptional Conditions.
- **OWASP API Security Top 10 2023**: BOLA, autenticação quebrada, autorização em nível de propriedade, consumo irrestrito de recursos, SSRF.
- **OWASP Top 10 for LLM Applications 2025** e **Top 10 for Agentic Applications 2026**: Prompt Injection, Sensitive Information Disclosure, Excessive Agency, Goal Hijack, Tool Misuse, Identity & Privilege Abuse, Memory/Context Poisoning, Insecure Inter-Agent Communication.
- **NIST AI RMF**, **NIST SSDF/SP 800-218**, **SP 800-218A** e **Zero Trust Architecture / SP 800-207**.

## Baseline por camada

| Tema | Baseline recomendado | Evidência de auditoria |
|---|---|---|
| Headers e hardening do browser | CSP ativa, headers declarados no Next.js, política explícita para conteúdo inline e terceiros | `next.config.js`, snapshot de resposta HTTP, relatório CSP |
| Segredos | Nenhum segredo no client bundle; `NEXT_PUBLIC_*` só para dados realmente públicos; segredos em vault/secret manager | scan do bundle, revisão de `.env*`, Gitleaks limpo |
| Banco | RLS em tudo que for acessível por cliente; grants mínimos; secret/service keys só server-side | políticas RLS, grants revisados, ausência de service key no front |
| Trânsito e repouso | TLS obrigatório; SSL enforcement quando disponível; rotação de chaves e segredos; criptografia adicional na aplicação para campos críticos | configuração de SSL, rotação documentada, classificação dos dados críticos |
| CORS e exposição de superfície | Allowlist por ambiente, separando APIs públicas de integrações server-to-server; nada de origem ampla por preguiça | matriz de origens permitidas e testes automatizados de preflight |
| Rate limiting e contenção | Limite por IP, usuário, tenant, webhook e ferramenta; limites de concorrência e orçamento para agentes | config de gateway, métricas de throttle, circuit breakers |
| Logging | Logs estruturados, com correlation IDs e redaction de PII por padrão; alertas para auth, falhas de autorização, segredos e anomalias | logging policy, SIEM/regras de alerta, amostras redigidas |
| n8n | Webhooks autenticados, pruning e redaction de execuções, `N8N_ENCRYPTION_KEY` padronizado, external secrets | variáveis de ambiente, prints de configuração, testes de webhook |
| Zero Trust | Sem confiança implícita por rede/localização; autenticação e autorização contínuas por recurso; foco em usuários, ativos e workflows | arquitetura, IAM, revisão periódica de privilégios |
| IA e agentes | Tool allowlist, memória escopada, aprovação humana para ações críticas, kill switch, inventário de modelos e provedores | catálogo de tools, políticas de aprovação, testes adversariais |

## Perguntas práticas por camada

### Frontend e camada web (Next.js)

- Há CSP configurada?
- Há segredo no bundle do cliente?
- Há dado pessoal demais no navegador ou em logs do cliente?

### APIs, webhooks e backends Python/Next.js

- Cada ID e campo retornado ou alterado pertence ao usuário/tenant certo?
- Há rate limiting e controle de consumo de recursos?
- Há validação de entrada e saída com schema forte?
- Há proteção contra SSRF em conectores, fetchers, crawlers e webhooks?
- Há logs e alertas auditáveis?

### Banco, auth e Supabase

- Toda tabela acessível pelo cliente tem RLS?
- O `service_role` ou secret key nunca vai para o browser?
- Há SSL enforcement?
- Segredos estão em Vault ou secret manager?
- Há rotina de rotação de chaves?

### Automações e n8n

- Existe `N8N_ENCRYPTION_KEY` próprio e consistente em todas as instâncias e workers?
- Webhooks exigem autenticação?
- Execuções antigas são podadas e dados sensíveis são redigidos?
- Credenciais centralizadas via external secrets quando aplicável?
- Instância publicada atrás de SSL, com MFA/SSO se o plano permitir?

### Camada de IA e agentes

- Quem controla o prompt?
- Quem escolhe as ferramentas?
- Qual o escopo de cada credencial?
- Que memória é persistida?
- Como o output vira ação?
- Existe separação entre leitura e escrita?
- Há validação programática do output?
- Há desligamento rápido do agente?
