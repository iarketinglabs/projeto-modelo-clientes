# Playbook de resposta a incidentes de segurança

## Base legal

A **Resolução CD/ANPD nº 15/2024** regulamentou a comunicação de incidente de segurança na LGPD. Em resumo:

- Comunique à **ANPD** quando o incidente puder causar **risco ou dano relevante** aos titulares.
- Comunique aos **titulares afetados** quando houver risco ou dano relevante.
- Prazo: **até 3 dias úteis**, contados conforme os arts. 6º e 9º do regulamento.

## Definição de incidente relevante

Um incidente é relevante quando houver:

- Acesso não autorizado a dados pessoais.
- Exposição, perda, alteração ou indisponibilidade de dados pessoais.
- Comprometimento de chaves, credenciais ou infraestrutura que proteja dados pessoais.
- Risco de dano aos titulares — financeiro, reputacional, discriminatório ou à privacidade.

## Passos do playbook

### 1. Contenção

- Isole o componente afetado (desative webhook, suspenda fluxo, bloqueie conta).
- Rotacione chaves, tokens e senhas comprometidos.
- Revogue sessões ativas e tokens de API.
- Preserve logs e snapshots antes que sejam perdidos.

### 2. Avaliação

- Identifique quais dados pessoais foram envolvidos (categorias e volume).
- Mapeie titulares afetados.
- Determine o escopo da exposição (quem teve acesso, por quanto tempo).
- Avalie probabilidade e gravidade do dano.
- Decida se o incidente é relevante para a ANPD/titulares.

### 3. Preservação de evidências

- Colete logs de aplicação, infraestrutura, n8n, Supabase e provedores de IA.
- Registre linha do tempo com horários, ações e responsáveis.
- Restrinja acesso às evidências aos investigadores autorizados.
- Evite alterar arquivos ou bancos envolvidos antes da coleta.

### 4. Notificação

Se o incidente for relevante:

- Prepare comunicação à ANPD dentro de **3 dias úteis**.
- Prepare comunicação aos titulares afetados, em linguagem clara, com:
  - natureza do incidente;
  - dados envolvidos;
  - medidas adotadas;
  - riscos para o titular;
  - canais de atendimento.

Mesmo que a notificação não seja obrigatória, documente a análise e a decisão.

### 5. Remediação

- Corrija a causa raiz (patch, configuração, RLS, autenticação, secret rotation).
- Re-execute scans de segurança.
- Valide o fix com testes automatizados e revisão manual.
- Atualize políticas, runbooks e guardrails de IA quando necessário.

### 6. Pós-incidente

- Elabore relatório pós-incidente com: resumo, linha do tempo, impacto, causa raiz, ações tomadas, lições aprendidas.
- Atualize o plano de resposta a incidentes.
- Revise retenção de logs e dados pessoais.
- Avalie se o incidente exige atualização do RIPD ou inventário de riscos.

## Modelo mínimo de registro

| Campo | Descrição |
|---|---|
| ID do incidente | Código único |
| Data/hora da descoberta |  |
| Data/hora do início | Quando possível determinar |
| Sistema afetado | n8n, Next.js, Supabase, API, agente, etc. |
| Dados envolvidos | Categorias e volume estimado |
| Titulares afetados | Quantidade e identificação |
| Descrição do incidente | O que aconteceu |
| Causa raiz | Técnica e/ou processual |
| Ações de contenção |  |
| Comunicação | ANPD, titulares, interna |
| Prazo de notificação | Dentro de 3 dias úteis? |
| Remediação | Correções aplicadas |
| Responsável | Nome e função |
| Status | Em investigação, contido, resolvido |

## Checklist de preparação

- [ ] Plano de resposta a incidentes documentado e acessível.
- [ ] Responsáveis e backups definidos.
- [ ] Canais de comunicação com ANPD e titulares mapeados.
- [ ] Templates de notificação pré-aprovados.
- [ ] Procedimento de rotação de segredos testado.
- [ ] Logs centralizados e com retenção adequada.
- [ ] Simulação de incidente realizada pelo menos anualmente.
