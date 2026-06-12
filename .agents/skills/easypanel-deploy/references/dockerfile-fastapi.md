# Dockerfile: Python API (FastAPI) no Easypanel

A API precisa escutar em `0.0.0.0` e na mesma porta informada no proxy do Easypanel (ex.: `8000`).

```dockerfile
# apps/api/Dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Pontos de atenção

- `--host 0.0.0.0` é essencial. Se a aplicação ouvir apenas em `127.0.0.1`, o proxy devolve 502.
- Mantenha `requirements.txt` no mesmo diretório do `Dockerfile`.
- Para outras stacks Python (Django, Flask etc.), mantenha o mesmo princípio: bind em `0.0.0.0` e porta alinhada ao proxy.
