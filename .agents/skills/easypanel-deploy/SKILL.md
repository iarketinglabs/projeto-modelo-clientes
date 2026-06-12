---
name: easypanel-deploy
description: Deploy Next.js, Python APIs, n8n, and Supabase on Easypanel with Docker, auto-deploy, and custom domains. Use this skill whenever the user mentions Easypanel, self-hosting, auto-deploy, Docker deploy, Next.js self-hosting, Python API hosting, n8n hosting, Supabase self-hosted, custom domain, or deploy automation for the Atomica project process.
---

# Easypanel Deploy para o processo Atomica

Guia operacional para subir a stack Atomica (Next.js + Python API + n8n + Supabase) no Easypanel com deploy automatizado e domínios customizados.

## Quando usar este skill

- O usuário pede para fazer deploy no Easypanel.
- O contexto envolve auto-deploy a partir do GitHub.
- Aparecem serviços como Next.js, FastAPI/Python, n8n ou Supabase.
- Há dúvidas sobre Dockerfile, portas, domínios, variáveis de ambiente ou troubleshooting.

## Pré-requisitos

- Servidor Linux limpo, com portas `80` e `443` livres.
- Docker e Easypanel instalados no host.
- Mínimo de 2 GB de RAM para o painel; a stack completa precisa de mais folga.
- Repositório GitHub acessível, com Dockerfile validado para Next.js e Python.
- Para auto-deploy: PAT fine-grained com `Metadata: read-only`, `Contents: read-only` e `Webhooks: read and write`.

Leia o checklist completo em [`references/checklist-pre-deploy.md`](references/checklist-pre-deploy.md).

## Arquitetura recomendada

Agrupe serviços stateless no mesmo projeto do Easypanel e isole o Supabase:

```
projeto: atomica-stack
├── web   (App Service, Next.js, Dockerfile, porta 3000)
├── api   (App Service, Python/FastAPI, Dockerfile, porta 8000)
└── n8n   (App Service, imagem oficial, porta 5678)

projeto: atomica-data
└── supabase (Compose Service, template oficial, endpoint via kong:8000)
```

Essa separação reduz o raio de impacto do Supabase, que é uma stack Compose pesada, e evita que o ciclo de deploy do frontend/backend reinicie o banco.

## Fluxo de deploy

### 1. Conectar o GitHub

1. Vá em **Settings > Github** no Easypanel.
2. Cole o PAT fine-grained com as permissões mínimas documentadas.
3. Alternativa: use Git SSH por serviço, copiando a chave SSH exibida na aba **Source** e cadastrando no repositório.

### 2. Criar o projeto e os serviços

1. Crie o projeto, por exemplo `atomica-stack`.
2. Adicione os App Services: `web`, `api` e `n8n`.
3. Para `web` e `api`, aponte a source para o repositório GitHub, selecione a branch de produção e, em monorepo, defina o `rootPath` (ex.: `apps/web`, `apps/api`).
4. Para o `n8n`, use o template oficial ou uma imagem Docker como `docker.n8n.io/n8nio/n8n:2.21.0`.
5. Crie um projeto separado `atomica-data` e adicione o Supabase como **Compose Service**, usando o template oficial do Easypanel.

### 3. Configurar build

- Para Next.js e Python, escolha **Dockerfile** como método de build.
- Isso reduz ambiguidade de autodetecção e torna o build reproduzível.

Veja os modelos de Dockerfile em:
- [`references/dockerfile-nextjs.md`](references/dockerfile-nextjs.md)
- [`references/dockerfile-fastapi.md`](references/dockerfile-fastapi.md)

### 4. Configurar variáveis de ambiente

- As variáveis da aba **Environment** ficam disponíveis em build-time e run-time.
- Use variáveis mágicas do Easypanel quando fizer sentido: `$(PROJECT_NAME)`, `$(SERVICE_NAME)`, `$(PRIMARY_DOMAIN)`.
- Em monorepos, a UI permite escolher o nome/caminho do arquivo `.env` usado no deploy.
- Nunca commite secrets no repositório; coloque-os diretamente na aba **Environment**.

### 5. Configurar domínios

1. Em **Domains & Proxy**, adicione o host customizado.
2. Informe a porta interna correta (`3000` para Next.js, `8000` para API, `5678` para n8n, `8000` para Supabase via `kong`).
3. Após o deploy, o Easypanel gera certificado Let's Encrypt automaticamente.

Modelos de preenchimento da UI para cada serviço estão em [`references/ui-templates.md`](references/ui-templates.md).

### 6. Ativar auto-deploy

1. Faça o deploy inicial manualmente e valide que o serviço responde no domínio.
2. Somente então ative **Auto Deploy**; o Easypanel adiciona um webhook no GitHub.
3. A cada push na branch selecionada, um novo deploy será iniciado.
4. Anote o **Deploy Webhook** do serviço para gatilhos externos (CMS, n8n etc.).

## Templates e referências

| Recurso | Quando ler |
|---|---|
| [`references/dockerfile-nextjs.md`](references/dockerfile-nextjs.md) | Para construir a imagem do frontend Next.js. |
| [`references/dockerfile-fastapi.md`](references/dockerfile-fastapi.md) | Para construir a imagem da API Python. |
| [`references/ui-templates.md`](references/ui-templates.md) | Para preencher a UI do Easypanel com templates de web, api, n8n e Supabase. |
| [`references/checklist-pre-deploy.md`](references/checklist-pre-deploy.md) | Antes de publicar ou entregar a stack. |
| [`references/troubleshooting.md`](references/troubleshooting.md) | Quando algo não sobe, não abre ou o auto-deploy não dispara. |

## Boas práticas

- Prefira Dockerfile para Next.js e Python; use o template oficial para n8n; trate Supabase como Compose separado.
- Ative auto-deploy somente depois do primeiro deploy saudável.
- Use projeto isolado para o Supabase para não misturar ciclo de vida com aplicações stateless.
- Se a equipe preferir menos operação, avalie usar Supabase Cloud e deixar no Easypanel apenas Next.js, API e n8n.
- Não prometa health checks avançados na UI do App Service além do que a documentação pública confirma; para casos críticos, use Compose Service ou `HEALTHCHECK` no Dockerfile.

## Troubleshooting rápido

- **502 / timeout / site não abre**: quase sempre é porta interna errada ou processo ouvindo em `localhost` em vez de `0.0.0.0`.
- **Auto-deploy não dispara**: serviço precisa estar funcionando, token precisa de permissão de Webhooks e branch correta precisa estar selecionada.
- **Next.js com internal server error**: use standalone + Dockerfile, não dependa de buildpack.

Para mais detalhes, leia [`references/troubleshooting.md`](references/troubleshooting.md).
