# Templates de configuração da UI do Easypanel

Use estas fichas como base ao criar cada serviço no painel. Substitua `org/repo`, domínios e credenciais pelos valores do projeto Atomica.

## Next.js (App Service)

```yaml
serviceType: app
serviceName: web
source:
  provider: github
  repository: org/repo
  branch: main
  rootPath: apps/web
build:
  method: Dockerfile
  dockerfilePath: apps/web/Dockerfile
environment: |
  NODE_ENV=production
  NEXT_TELEMETRY_DISABLED=1
  # Adicione outras variáveis do projeto aqui
domains:
  - host: app.example.com
    proxyPort: 3000
deploy:
  replicas: 1
  autoDeploy: true
```

## Python API (App Service)

```yaml
serviceType: app
serviceName: api
source:
  provider: github
  repository: org/repo
  branch: main
  rootPath: apps/api
build:
  method: Dockerfile
  dockerfilePath: apps/api/Dockerfile
environment: |
  ENV=production
  LOG_LEVEL=info
  # Adicione DATABASE_URL e outras secrets aqui
domains:
  - host: api.example.com
    proxyPort: 8000
deploy:
  replicas: 1
  autoDeploy: true
```

## n8n (App Service com imagem)

```yaml
serviceType: app
serviceName: n8n
source:
  type: image
  image: docker.n8n.io/n8nio/n8n:2.21.0
environment: |
  N8N_HOST=n8n.example.com
  N8N_PORT=5678
  N8N_PROTOCOL=https
  N8N_PROXY_HOPS=1
  WEBHOOK_URL=https://n8n.example.com/
  DB_TYPE=postgresdb
  DB_POSTGRESDB_HOST=postgres.example.internal
  DB_POSTGRESDB_PORT=5432
  DB_POSTGRESDB_DATABASE=n8n
  DB_POSTGRESDB_USER=n8n
  DB_POSTGRESDB_PASSWORD=troque-isto
  # Se for escalar com queue mode, adicione Redis aqui
domains:
  - host: n8n.example.com
    proxyPort: 5678
mounts:
  - type: volume
    name: data
    mountPath: /home/node/.n8n
deploy:
  replicas: 1
```

### Dicas do n8n

- `WEBHOOK_URL` deve ser o domínio público em `https://`.
- `N8N_PROXY_HOPS=1` é recomendado quando o n8n fica atrás do proxy reverso do Easypanel.
- O volume em `/home/node/.n8n` preserva workflows e credenciais entre deploys.
- MySQL/MariaDB foram descontinuados pelo n8n; prefira PostgreSQL.

## Supabase (Compose Service)

```yaml
serviceType: compose
serviceName: supabase
source:
  type: git
  repo: https://github.com/easypanel-io/compose.git
  ref: 18-05-2026
  rootPath: /supabase/code
  composeFile: docker-compose.yml
domains:
  - host: supabase.example.com
    service: kong
    proxyPort: 8000
deploy:
  autoDeploy: false
```

### Dicas do Supabase

- O endpoint público passa pelo serviço `kong` na porta `8000`, não diretamente pelo Postgres.
- Não ative auto-deploy no Supabase; mantenha o deploy manual para evitar reinicializações acidentais da stack.
- Considere rodar o Supabase em projeto separado para reduzir o raio de impacto operacional.
