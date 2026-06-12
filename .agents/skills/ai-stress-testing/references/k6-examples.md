# Exemplos k6

## Stress de API com rampa, spike e invariantes de negócio

```js
import http from 'k6/http';
import { check } from 'k6';
import { Counter, Trend } from 'k6/metrics';

const businessFailures = new Counter('business_failures');
const businessLatency = new Trend('business_latency', true);

export const options = {
  scenarios: {
    api_stress: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      maxVUs: 400,
      stages: [
        { target: 50, duration: '2m' },   // warm-up
        { target: 150, duration: '5m' },  // ramp
        { target: 300, duration: '30s' }, // spike
        { target: 150, duration: '10m' }, // sustain
        { target: 0, duration: '1m' }     // cool-down
      ],
      tags: { suite: 'api_stress' }
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800', 'p(99)<1500'],
    dropped_iterations: ['count<10'],
    business_failures: ['count==0']
  },
  summaryTrendStats: ['min', 'avg', 'med', 'p(95)', 'p(99)', 'max']
};

export default function () {
  const baseUrl = __ENV.BASE_URL;
  const token = __ENV.BEARER_TOKEN;
  const importId = `stress-${__VU}-${__ITER}-${Date.now()}`;

  const authHeaders = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': importId
  };

  const createRes = http.post(
    `${baseUrl}/api/imports`,
    JSON.stringify({
      source: 'stress-test',
      records: Array.from({ length: 100 }, (_, i) => ({
        external_id: `${importId}-${i}`,
        amount: i
      }))
    }),
    {
      headers: authHeaders,
      tags: { endpoint: 'imports_create' }
    }
  );

  businessLatency.add(createRes.timings.duration, { endpoint: 'imports_create' });

  const createOk = check(
    createRes,
    {
      'imports_create accepted': (r) => [200, 201, 202].includes(r.status)
    },
    { endpoint: 'imports_create' }
  );

  if (!createOk) {
    businessFailures.add(1, { endpoint: 'imports_create' });
  }

  const listRes = http.get(
    `${baseUrl}/api/items?page=1&pageSize=100&sort=-created_at`,
    {
      headers: { Authorization: `Bearer ${token}` },
      tags: { endpoint: 'items_list' }
    }
  );

  businessLatency.add(listRes.timings.duration, { endpoint: 'items_list' });

  const listOk = check(
    listRes,
    {
      'items_list status 200': (r) => r.status === 200
    },
    { endpoint: 'items_list' }
  );

  if (!listOk) {
    businessFailures.add(1, { endpoint: 'items_list' });
  }
}

export function handleSummary(data) {
  return {
    'stress-summary.json': JSON.stringify(data, null, 2)
  };
}
```

Comando:

```bash
BASE_URL=https://staging.example.com BEARER_TOKEN=xxx k6 run stress-api.js
```

## Race condition em duplicate submit / replay

```js
import http from 'k6/http';
import { check } from 'k6';
import { Counter } from 'k6/metrics';

const duplicateCreates = new Counter('duplicate_creates');

export const options = {
  scenarios: {
    same_user_burst: {
      executor: 'constant-vus',
      vus: 20,
      duration: '1m',
      tags: { suite: 'race_condition' }
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    duplicate_creates: ['count==0']
  }
};

export default function () {
  const baseUrl = __ENV.BASE_URL;
  const token = __ENV.BEARER_TOKEN;
  const key = `order-${__VU}-${__ITER}`;

  const makeReq = () => ({
    method: 'POST',
    url: `${baseUrl}/api/orders`,
    body: JSON.stringify({
      cart_id: `cart-${__VU}`,
      checkout_token: key
    }),
    params: {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Idempotency-Key': key
      },
      tags: {
        endpoint: 'orders_create',
        pattern: 'duplicate_submit'
      }
    }
  });

  const responses = http.batch([
    makeReq(),
    makeReq(),
    makeReq(),
    makeReq(),
    makeReq()
  ]);

  const allHandled = check(responses, {
    'every response is known': (rs) =>
      rs.every((r) => [200, 201, 202, 409].includes(r.status))
  });

  const createdCount = responses.filter((r) => [200, 201].includes(r.status)).length;

  if (allHandled && createdCount > 1) {
    duplicateCreates.add(createdCount - 1, {
      endpoint: 'orders_create'
    });
  }
}
```

Comando:

```bash
BASE_URL=https://staging.example.com BEARER_TOKEN=xxx k6 run race-orders.js
```

## Observações

- Para 1M+ itens, semeiere o dataset antes e estresse apenas paginação, busca, ordenação, export e filtros.
- Monitore o próprio load generator: falta de VUs ou gargalo do host aparece como `dropped_iterations`.
