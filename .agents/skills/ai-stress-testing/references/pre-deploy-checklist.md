# Checklist Pré-Deploy de Stress Test

Marque cada item antes de executar stress de verdade em pré-deploy.

- [ ] **OpenAPI, HAR, exemplos de payload e regras de auth estão versionados no mesmo commit do teste**; o LLM não está inventando endpoint, header ou campo.
- [ ] **Rotas do Next.js foram separadas em pacotes cacheados vs dinâmicos**, para não misturar `GET` com comportamento de cache e `POST/PATCH/DELETE` sem cache no mesmo resultado.
- [ ] **A estratégia de conexão do Supabase foi escolhida explicitamente** — pooler de app ou Supavisor — e o teste observa conexões máximas e latência de pool.
- [ ] **O n8n roda em `queue mode` quando a carga de workflow exigir escala**, e o teste mede tanto a entrada no webhook quanto o throughput dos workers.
- [ ] **Endpoints sensíveis de `POST` e `PATCH` documentam e testam `Idempotency-Key`**, incluindo política de expiração e replay.
- [ ] **O pacote OWASP mínimo entrou no plano**: duplicate submit, mesmo recurso em concorrência, concurrent sessions e workflow order bypass.
- [ ] **Thresholds e invariantes de negócio estão codificados**, e não só "observados no olho". Em k6: thresholds. Em Artillery: `ensure`.
- [ ] **Volume extremo foi modelado corretamente**: massa pré-semeada para 1M+ itens; ingestão em lotes controlados para 10k+ registros; nada de medir o load generator por acidente.
- [ ] **Se houver hooks de setup/teardown no Artillery distribuído, eles são idempotentes**, porque `before` e `after` rodam uma vez por worker.
- [ ] **Os resultados vão virar artifact**, não só stdout: JSON do k6, CSV do Locust, dashboard do JMeter, e preferência por envio a Prometheus/OTel.
- [ ] **O workflow está no CI**, com gatilhos separados para PR, staging e rotinas noturnas/semanais.
