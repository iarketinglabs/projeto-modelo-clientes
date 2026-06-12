# Checklist pré-deploy no Easypanel

Preencha antes de colocar qualquer serviço em produção.

## Infraestrutura

- [ ] Servidor Linux limpo, sem serviços ocupando as portas `80` e `443`.
- [ ] Docker e Easypanel instalados no host.
- [ ] Mínimo de 2 GB de RAM para o painel; para a stack completa (Next.js + API + n8n + Supabase), prevê-se folga adicional.
- [ ] Portas 80 e 443 liberadas no firewall do servidor/cloud.

## Git e auto-deploy

- [ ] GitHub conectado em **Settings > Github**.
- [ ] PAT fine-grained com permissões mínimas:
  - Metadata: read-only
  - Contents: read-only
  - Webhooks: read and write (necessário para auto-deploy)
- [ ] Alternativa: chave SSH do serviço cadastrada no repositório/organização.
- [ ] Branch de produção selecionada no source do serviço.

## Aplicações

- [ ] Next.js configurado com `output: "standalone"` e `HOSTNAME=0.0.0.0`.
- [ ] API Python iniciada com `--host 0.0.0.0` e porta alinhada ao proxy.
- [ ] n8n com `WEBHOOK_URL` público em HTTPS e `N8N_PROXY_HOPS=1`.
- [ ] Supabase publicado via `kong:8000` (Compose Service).

## Domínios e licença

- [ ] DNS apontando para o IP do servidor.
- [ ] Se usar wildcard ou domínio automático por serviço: licença paga ativa.
- [ ] Backup nativo de banco requer plano Hobby ou superior.

## Operação

- [ ] Primeiro deploy realizado manualmente e validado.
- [ ] Auto-deploy ativado somente após o primeiro deploy saudável.
- [ ] Deploy Webhook de cada serviço anotado para automações externas.
- [ ] Variáveis de ambiente sensíveis revisadas antes de subir.
