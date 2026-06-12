# Catálogo de Edge Cases por Tipo de Sistema

Use este catálogo para garantir que nenhum cenário crítico seja esquecido durante a Leva 4 da entrevista. Para cada tipo de sistema ou funcionalidade, verifique os edge cases aplicáveis.

---

## 1. Autenticação e Autorização

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 1.1 | Usuário insere senha incorreta repetidamente | Bloquear após N tentativas; notificar email; cooldown progressivo |
| 1.2 | Token/JWT expira durante operação | Preservar estado/rascunho; redirecionar para login; retomar após reauth |
| 1.3 | Usuário tenta acessar recurso sem permissão | Retornar 403; log de tentativa; não revelar existência do recurso (404 preferível se sensível) |
| 1.4 | Login em dispositivo novo/locais suspeitos | Notificar usuário; exigir 2FA; email de alerta de segurança |
| 1.5 | Usuário esquece senha e solicita reset múltiplas vezes | Invalidar links anteriores; expirar link em 15-60 min; rate limit por email |
| 1.6 | Conta desativada/excluída tenta login | Mensagem genérica (não revelar se conta existe); direcionar para suporte |
| 1.7 | Session hijacking detectado | Invalidar todas as sessões; forçar reauth; notificar usuário |
| 1.8 | OAuth/SSO provider indisponível | Fallback para login local (se configurado); mensagem informativa; retry manual |

---

## 2. Formulários e Inputs

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 2.1 | Campo obrigatório vazio | Mensagem de erro clara indicando campo; focar no campo; não limpar outros dados |
| 2.2 | Dados em formato inválido (email, CPF, data) | Validar no cliente e servidor; mensagem específica por formato; exemplos de formato correto |
| 2.3 | Injection attempts (XSS, SQLi, NoSQLi) | Sanitizar input; validar charset; rejeitar padrões suspeitos; log de segurança |
| 2.4 | Input com caracteres especiais/emoji/unicode | Aceitar se válido para o domínio; normalizar NFC; definir charset aceito |
| 2.5 | Input excede tamanho máximo | Rejeitar com erro claro; indicar limite; não truncar silenciosamente |
| 2.6 | Upload de arquivo com extensão/ MIME type spoofing | Validar magic bytes; rejeitar mime mismatch; scan de malware se aplicável |
| 2.7 | Usuário preenche formulário, perde conexão e reconecta | Autosave em intervalos; recuperar rascunho ao retornar; indicar dados salvos |
| 2.8 | Duplo submit do formulário | Idempotency key; desabilitar botão após primeiro click; detectar duplicata no servidor |
| 2.9 | Formulário multistep — usuário volta para etapa anterior | Preservar dados já informados; permitir edição; validar novamente ao avançar |
| 2.10 | Campos condicionais — dependências não satisfeitas | Ocultar/mostrar campos dinamicamente; validar consistência de estado no servidor |

---

## 3. APIs e Integrações

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 3.1 | API externa retorna timeout | Retry com exponential backoff (máx 3x); circuit breaker após falhas consecutivas; fallback/cache |
| 3.2 | API externa retorna 5xx | Tratar como indisponível; fallback; notificar operação; não propagar erro cru para usuário |
| 3.3 | API externa retorna 4xx | Logar detalhes; não retry automaticamente (exceto 429); mensagem amigável ao usuário |
| 3.4 | Rate limit atingido (429) | Retry com backoff respeitando Retry-After; fila assíncrona; informar usuário sobre delay |
| 3.5 | Payload muito grande (413) | Chunking/streaming; validar tamanho antes de enviar; mensagem informativa |
| 3.6 | Resposta da API com schema inesperado | Schema validation; fallback para campo default; alertar operação; não quebrar fluxo |
| 3.7 | Webhook delivery falha | Retry automático com backoff; dead letter queue; notificar admin após N falhas |
| 3.8 | Webhook recebido duplicado | Idempotency key; verificar se já processado; retornar 200 sem reprocessar |
| 3.9 | API versão deprecada | Detectar versão; migrar automaticamente se possível; alertar operação |
| 3.10 | Contrato de API muda breaking change | Versionamento; validação de contrato; testes de contrato (consumer-driven) |

---

## 4. Pagamentos e Transações Financeiras

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 4.1 | Pagamento aprovado mas webhook de confirmação não chega | Reconciliação assíncrona; polling de status; notificar admin após timeout |
| 4.2 | Usuário fecha browser durante processamento de pagamento | Webhook continua processando; notificar por email/SMS resultado; permitir consulta de status |
| 4.3 | Duplo clique em "pagar" | Idempotency key no gateway; desabilitar botão; verificar transação existente por sessão |
| 4.4 | Cartão recusado com erro genérico | Mapear códigos de erro do gateway; mensagem informativa sem expor detalhes internos |
| 4.5 | Reembolso parcial solicitado | Suportar valor parcial; recalcular saldo; notificar usuário; atualizar relatórios |
| 4.6 | Concorrência — estoque acaba entre adicionar ao carrinho e pagar | Reserva temporária de estoque; validar disponibilidade antes de cobrar; notificar indisponibilidade |
| 4.7 | Cancelamento de assinatura no meio do período pagamento | Manter acesso até fim do período; não reembolsar proporcional (ou regras claras); downgrade controlado |
| 4.8 | Fraude detectada (chargeback posterior) | Bloquear conta temporariamente; revisão manual; integrar com antifraude; log para análise |

---

## 5. Uploads e Arquivos

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 5.1 | Upload de arquivo malicioso (exe, js, zip bomb) | Whitelist de extensões; validar MIME e magic bytes; scan antivírus; rejeitar se suspeito |
| 5.2 | Upload interrompido (conexão cai no meio) | Resume upload (chunked); permitir retry; limpar arquivos incompletos após timeout |
| 5.3 | Arquivo maior que o limite do servidor | Validar antes de iniciar upload; mensagem clara com limite; progress bar realista |
| 5.4 | Nome de arquivo com caracteres especiais/path traversal | Sanitizar nome; rejeitar paths relativos; gerar nome único no storage |
| 5.5 | Múltiplos uploads simultâneos | Fila de processamento; limitar concorrência; feedback de progresso individual |
| 5.6 | Arquivo corrompido | Validar checksum/integrity; rejeitar com erro; solicitar reenvio |
| 5.7 | Storage cheio ou indisponível | Retry com backoff; notificar operação; fila para reprocessamento; mensagem ao usuário |

---

## 6. Notificações (Email, SMS, Push)

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 6.1 | Email rejeitado (bounce hard/soft) | Hard bounce: desativar email; soft bounce: retry 3x; atualizar status do contato |
| 6.2 | SMS não entregue | Retry com outro provider; notificar por push/email alternativo; log de falha |
| 6.3 | Usuário desativa notificações | Respeitar preferência imediatamente; não enviar; registrar opt-out |
| 6.4 | Template de notificação com variável ausente | Fallback para default; não enviar com placeholder cru; log de erro de template |
| 6.5 | Volume massivo de notificações (milhões) | Fila assíncrona; rate limiting por provider; batching; priorização de fila |
| 6.6 | Notificação duplicada | Idempotency key; verificar se já enviado no período; deduplicação na fila |

---

## 7. Busca, Listagens e Paginação

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 7.1 | Busca com termo muito genérico (retorna milhares) | Limitar resultados; sugerir filtros; autocomplete inteligente; timeout de busca |
| 7.2 | Busca sem resultados | Sugerir termos alternativos; mostrar categorias populares; não retornar erro 500 |
| 7.3 | Paginação — usuário solicita página inexistente | Retornar última página válida ou vazio com metadados; não quebrar |
| 7.4 | Ordenação por campo inválido | Default seguro; ignorar parâmetro inválido; log para análise |
| 7.5 | Listagem com milhões de registros | Cursor-based pagination; não offset profundo; índices otimizados; cache |
| 7.6 | Filtros combinados retornam zero resultados | Indicar qual filtro está causando; permitir remover filtros um a um |
| 7.7 | Exportação de dados grandes (CSV/Excel) | Streaming assíncrono; notificar quando pronto; não bloquear UI; limite de linhas |

---

## 8. Concorrência, Estados e Sincronização

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 8.1 | Dois usuários editam mesmo registro simultaneamente | Optimistic locking; detectar conflito; apresentar diff; permitir merge manual |
| 8.2 | Race condition em checkout/compra | Lock pessimista ou fila; validar estado atual antes de commit; não duplicar pedido |
| 8.3 | Processo assíncrono falha no meio (job queue) | Retry com limite; dead letter queue; notificar admin; manter estado parcial se possível |
| 8.4 | Sistema reinicia durante operação crítica | Recuperar estado do journal/log; idempotência; rollback se necessário |
| 8.5 | Dados desatualizados em cache vs banco | TTL adequado; cache invalidation strategy; stale-while-revalidate se aplicável |
| 8.6 | Clock skew entre servidores distribuídos | NTP sync; usar timestamps monotônicos; ordenação por sequência lógica, não apenas tempo |

---

## 9. Internacionalização e Localização

| # | Edge Case | Comportamento Esperado Típico |
|---|---|---|
| 9.1 | Idioma não suportado pelo usuário | Fallback para idioma padrão; permitir seleção manual; não quebrar layout |
| 9.2 | Formato de data/hora/moeda diverso | Localizar por locale do usuário; não hardcode formatos; usar bibliotecas standard |
| 9.3 | Texto traduzido muito longo e quebra layout | Layout flexível; truncar com ellipsis se necessário; testar em todos os idiomas suportados |
| 9.4 | RTL (Right-to-Left) languages | Suporte a direção de texto; mirror de layouts; testar com árabe/hebraico |
| 9.5 | Fuso horário do usuário vs servidor | Armazenar em UTC; exibir em local time; considerar DST (horário de verão) |

---

## Como usar este catálogo

1. Identifique quais categorias se aplicam ao sistema em questão.
2. Durante a Leva 4 da entrevista, percorra os itens aplicáveis e pergunte ao usuário o comportamento esperado.
3. Não assuma o comportamento padrão — sempre valide com o usuário ou documente a decisão tomada.
4. Adicione edge cases específicos do domínio que não estejam neste catálogo genérico.
