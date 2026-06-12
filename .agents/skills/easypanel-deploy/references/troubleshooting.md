# Troubleshooting no Easypanel

## Build conclui, mas o serviço devolve 502 / timeout / não abre

Causa mais comum: porta interna ou binding errado.

- Confirme que o processo escuta em `0.0.0.0`, não em `127.0.0.1` ou `localhost`.
- Verifique se a porta em **Domains & Proxy > Proxy Port** é igual à porta exposta no `Dockerfile`.
- Para Next.js standalone: use `HOSTNAME=0.0.0.0`.
- Para FastAPI/Uvicorn: use `--host 0.0.0.0`.

## Auto-deploy não dispara

- O serviço precisa estar totalmente configurado e com um deploy inicial bem-sucedido.
- O token GitHub precisa ter permissão **Webhooks: read and write**.
- A branch correta precisa estar selecionada na aba **Source**.

## Deploy Webhook não gera novo build

O webhook inicia um deploy, mas se o repositório não teve mudança de código, o Docker pode reutilizar camadas cacheadas e o artefato não se altera.

- Workaround comunitário: adicione uma variável `CACHEBUST` no `Dockerfile` e incremente-a quando precisar forçar recompilação.
- Use isso principalmente para rebuilds disparados por CMS ou automações externas.

## Next.js com internal server error

- Evite builds via autodetecção/buildpack para aplicações SSR.
- Use Dockerfile com `output: "standalone"` e o fluxo documentado no `dockerfile-nextjs.md`.

## Health checks no App Service

A documentação pública do Easypanel não confirma de forma explícita um seletor de health check na UI do App Service com modos HTTP/TCP/command. Health checks Docker/Compose são confirmados no template oficial do Supabase.

- Se health check rigoroso for exigido, prefira Compose Service ou Dockerfile com instrução `HEALTHCHECK`.

## Limites de plano

- Plano Free permite até 3 projetos, serviços/deploys ilimitados e monitoramento básico.
- Backup de banco e custom service domain exigem plano pago (Hobby ou superior).
- Cluster ainda consta como *under development* no plano Business.
