# Dockerfile: Next.js no Easypanel

Use `output: "standalone"` no `next.config.js` e ouça em `0.0.0.0` na porta exposta (normalmente `3000`). O standalone gera uma imagem mínima e evita inconsistências entre build e runtime.

```dockerfile
# apps/web/Dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV HOSTNAME=0.0.0.0
ENV PORT=3000

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

## Pontos de atenção

- `HOSTNAME=0.0.0.0` é obrigatório para o proxy do Easypanel alcançar o container.
- A porta do `EXPOSE` deve ser a mesma configurada em **Domains & Proxy > Proxy Port**.
- Em monorepos, o `rootPath` do App Service geralmente é `apps/web` e o `Dockerfile` fica dentro dele.
