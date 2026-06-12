# Modelagem de ameaças para agentes de IA

## Abordagem recomendada

Misture três frameworks:

- **STRIDE** — ameaças clássicas de segurança (Microsoft SDL).
- **LINDDUN** — ameaças de privacidade desde a arquitetura.
- **OWASP GenAI / Agentic** — riscos específicos de LLMs e agentes.

NIST AI RMF, NIST SSDF/SP 800-218 e SP 800-218A ajudam a estender o raciocínio para o ciclo de vida de IA e desenvolvimento seguro.

A pergunta central em agentes não é apenas “quem pode entrar?”, mas “quem pode fazer o quê, em nome de quem, com qual memória, usando qual ferramenta, e com que possibilidade de reversão?”.

## Template STRIDE adaptado para IA

| Ativo ou fluxo | Pergunta de ameaça | Exemplo realista em IA/automação | Controle esperado |
|---|---|---|---|
| Entrada do usuário, ticket, formulário ou webhook | **Spoofing / Prompt Injection / Unawareness**: quem está falando, e o sistema sabe que está falando com IA? | Um e-mail ou ticket injeta instruções para o agente ignorar políticas e buscar dados de outro cliente | Auth no ingresso, classificação de canal confiável, sanitização de input, disclosure de interação com IA, guardrails de prompt |
| Ferramentas do agente | **Elevation of Privilege / Tool Misuse** | O agente usa credencial ampla para criar, excluir ou exportar registros no CRM/banco | Scopes mínimos por ferramenta, chaves separadas, aprovação humana para escrita destrutiva, segregação read/write |
| Memória, vector store e histórico | **Tampering / Data Disclosure / Linking** | Memória contaminada por um usuário passa a influenciar respostas para outro tenant | Escopo por tenant, TTL, limpeza de memória, redaction, indexação com separação forte de contexto |
| Output do modelo | **Integrity / Insecure Output Handling** | Resposta do modelo vira query, comando ou decisão operacional sem validação | Output parser estrito, allowlist de comandos, validação de esquema, HITL para ações críticas |
| Logs, traces e analytics | **Repudiation / Data Disclosure / Non-compliance** | Payloads com CPF, e-mail ou histórico de conversa ficam salvos em observabilidade e n8n | Redaction por padrão, retenção mínima, acesso restrito, trilha de auditoria e alertas |
| Dependências, modelos e conectores | **Supply Chain / Integrity Failures** | Biblioteca, MCP server, imagem Docker ou dataset introduz comportamento malicioso | SBOM, pinning, assinatura/verificação quando possível, scan contínuo de dependências e imagens, inventário de componentes |

## Template mínimo de threat modeling

Use estes tópicos para documentar cada sistema ou fluxo:

1. **Contexto do sistema** — o que faz, quem usa, qual o valor de negócio.
2. **Atores internos/externos** — usuários, admins, agentes, terceiros, modelos.
3. **Dados pessoais e sensíveis** — categorias, volumes, fluxos.
4. **Bases legais** — por fluxo.
5. **Fronteiras de confiança** — rede, tenant, ambiente, infraestrutura.
6. **Ferramentas e integrações do agente** — lista, escopo, credenciais.
7. **Riscos STRIDE** — por ativo/fluxo.
8. **Riscos LINDDUN** — por ativo/fluxo.
9. **Riscos GenAI/Agentic** — prompt injection, excessive agency, goal hijack, tool misuse, memory poisoning, identity/privilege abuse.
10. **Controles existentes** — o que já está implementado.
11. **Gaps** — o que falta cobrir.
12. **Evidências** — prints de config, políticas, testes.
13. **Decisão de aceite de risco** — quem decide, em que data, com quais compensações.

## Checklist rápido de modelagem

- [ ] Liste todos os atores que interagem com o sistema.
- [ ] Mapeie cada fluxo de dados pessoais de ponta a ponta.
- [ ] Desenhe fronteiras de confiança (navegador, edge, servidor, banco, terceiros).
- [ ] Aplique STRIDE em cada fronteira.
- [ ] Aplique LINDDUN quando houver coleta, armazenamento ou compartilhamento de dados pessoais.
- [ ] Aplique OWASP GenAI/Agentic para prompts, ferramentas, memória e outputs.
- [ ] Documente controles e gaps.
- [ ] Registre decisões de aceite de risco com dono e data.
