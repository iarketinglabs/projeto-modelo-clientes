# Exemplo Artillery + Playwright

Use este padrão para jornadas críticas de frontend no Next.js quando precisar medir Web Vitals sob carga real.

```ts
import { Page, expect } from '@playwright/test';

const baseUrl = process.env.BASE_URL || 'http://localhost:3000';

export const config = {
  target: baseUrl,
  phases: [
    { duration: '2m', arrivalRate: 1, rampTo: 5, name: 'warmup' },
    { duration: '5m', arrivalRate: 5, rampTo: 20, name: 'ramp' },
    { duration: '30s', arrivalRate: 40, name: 'spike' }
  ],
  engines: {
    playwright: {
      extendedMetrics: true
    }
  }
};

export const scenarios = [
  {
    engine: 'playwright',
    testFunction: checkoutFlow
  }
];

async function checkoutFlow(page: Page) {
  await page.goto(`${baseUrl}/checkout`);

  await page.getByLabel(/email/i).fill(`stress+${Date.now()}@example.com`);
  await page.getByRole('button', { name: /continuar/i }).click();

  await page.getByRole('button', { name: /finalizar pedido/i }).click();

  await expect(
    page.getByText(/pedido recebido|order confirmed/i)
  ).toBeVisible();
}
```

Comando:

```bash
BASE_URL=https://staging.example.com npx artillery run checkout-flow.yml
```

## Pontos de atenção

- Testes de API isolados não garantem performance percebida pelo usuário.
- Playwright em carga mede a aplicação no nível certo de abstração e coleta Web Vitals automaticamente.
- Se já existir suite Playwright de E2E, esse caminho costuma ser o mais rápido para transformar teste funcional em stress browser-centric.
- Normalize nomes dinâmicos de métricas no Playwright com `$rewriteMetricName` quando query strings ou IDs explodirem a cardinalidade.
