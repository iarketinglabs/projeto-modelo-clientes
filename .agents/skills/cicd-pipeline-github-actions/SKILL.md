---
name: cicd-pipeline-github-actions
description: Design and maintain CI/CD pipelines with GitHub Actions for the Atomica monorepo (Next.js + Python + n8n + Supabase). Use this skill whenever the user asks about CI/CD, GitHub Actions workflows, pipeline setup, lint/test/build automation, deploy automation, Easypanel deploy webhook, reusable workflows, change detection, parallel jobs, smoke tests, branch protection gates, failure notifications, or secrets governance for the project.
---

# CI/CD Pipeline with GitHub Actions

Use this skill to design, review, or fix CI/CD pipelines for the Atomica monorepo. The stack combines Next.js (`apps/web`), Python (`apps/api`), n8n (`apps/n8n`), and Supabase (`supabase`). The recommended target host is Easypanel, triggered by deploy webhooks.

The goal is a pipeline that runs on every pull request and push, detects which parts of the monorepo changed, validates them in parallel, and only deploys after a quality gate passes.

## When to use this skill

- The user asks for a GitHub Actions workflow for the project.
- The topic is lint, test, build, or deploy automation.
- The user mentions Easypanel webhook, auto-deploy, or deploy trigger.
- The user is debugging a stuck PR check, a missing secret, a failed deploy, or a skipped job.
- The user wants reusable workflows, matrix jobs, concurrency control, or notifications.

## Core architecture

Use one always-on CI workflow and one reusable deploy workflow.

- **Always run the CI workflow** on `pull_request`, `push` to protected branches, and `workflow_dispatch`. Do not rely on `paths` filters for required checks, because skipped workflows can leave branch-protection checks stuck in "Pending".
- **Detect changes inside the workflow** and expose boolean outputs. Downstream jobs run only when their area changed.
- **Run jobs in parallel** per stack (web, api, n8n, supabase) with matrix strategies for Node.js and Python versions.
- **Separate deploy from CI** with a reusable workflow called only from `main` after the quality gate passes. This keeps deployment logic centralized and reviewable.
- **Use GitHub Environments** for staging and production, with environment-scoped secrets and optional required reviewers.

For the Easypanel side of the setup, read [`references/easypanel-deploy-skill-link.md`](references/easypanel-deploy-skill-link.md).

## Change detection

Detect changes in a dedicated job at the start of the CI workflow. Compare the current commit against:

- `github.event.pull_request.base.sha` for pull requests.
- `github.event.before` for pushes.

If no valid base SHA exists, such as the first commit on a branch, mark all deployable areas as changed to stay safe.

Map file paths to stacks:

| Path pattern | Stack |
|---|---|
| `apps/web/*`, `packages/ui/*`, `packages/config/*` | web |
| `apps/api/*`, `packages/python-common/*` | api |
| `apps/n8n/*`, `docker/n8n/*` | n8n |
| `supabase/*` | supabase |
| Root lockfiles (`package-lock.json`, `pnpm-lock.yaml`, etc.) | web |
| Root Python lockfiles (`requirements.txt`, `pyproject.toml`, etc.) | api |
| Shared root files (`docker/*`, `.github/workflows/*`) | web, api, n8n |

Expose one output per stack and one `deploy_changed` output that is true when any deployable area changed.

Read the full detection script and template in [`references/ci-yml-template.md`](references/ci-yml-template.md).

## Parallel jobs per stack

After change detection, run independent jobs for each changed stack. This keeps feedback fast and makes failures easy to read.

### Next.js (`apps/web`)

- Install dependencies with `npm ci` or equivalent package manager.
- Run `npm run lint` using ESLint CLI directly. Do not rely on `next lint` or build-time lint; newer Next.js versions do not run lint during build.
- Run tests with `npm run test`.
- Run `npm run build` as a build verification step.
- Use a matrix for Node.js versions, such as `[20, 22]`.

### Python API (`apps/api`)

- Install dependencies from `requirements.txt` and `requirements-dev.txt`.
- Run `ruff check .` for lint.
- Run `black --check .` or `ruff format --check .` for format verification.
- Run `pytest -q` for tests.
- Use a matrix for Python versions, such `["3.11", "3.13"]`.

### n8n

- If the project customizes n8n with a Dockerfile or versioned artifacts, run a Docker build verification.
- If n8n is used without customization, the CI job can be minimal or omitted; the deploy still uses a webhook and smoke test.

### Supabase

- Start the local stack with `supabase db start`.
- Run `supabase db lint --level error`.
- Run `supabase test db`.

### Docker verification

Build Docker images for web, api, and n8n with `docker/build-push-action`, `push: false`, and GitHub Actions cache. This catches Dockerfile regressions without publishing images.

## Quality gate

Add a final job named `quality-gate` that depends on all stack jobs and Docker verification jobs. Use `if: always()` and check each dependency result. Accept `success` or `skipped`; fail on anything else.

This pattern guarantees that the gate reports a clear outcome even when some jobs are skipped because their stack did not change.

## Reusable deploy workflow

Create `deploy.yml` under `.github/workflows/` as a reusable workflow (`on: workflow_call`) and also support manual triggers (`on: workflow_dispatch`).

Inputs:

| Input | Type | Purpose |
|---|---|---|
| `environment` | string | Target GitHub Environment (`staging` or `production`) |
| `deploy_web` | boolean | Trigger web deploy webhook |
| `deploy_api` | boolean | Trigger api deploy webhook |
| `deploy_n8n` | boolean | Trigger n8n deploy webhook |
| `deploy_supabase` | boolean | Apply Supabase migrations |

Use `concurrency` with `group: deploy-${{ inputs.environment }}` to serialize deployments per environment. Set the job `environment` to the input so environment secrets and protection rules apply.

The deploy job runs after CI calls it from `main` and passes `secrets: inherit`.

Read the full template in [`references/deploy-yml-template.md`](references/deploy-yml-template.md).

## Triggering Easypanel deploy webhooks

For explicit control, trigger Easypanel deploys from the reusable workflow using service-specific Deploy Webhooks.

- Store each webhook URL as an environment secret, for example `EASYPANEL_WEB_DEPLOY_WEBHOOK`, `EASYPANEL_API_DEPLOY_WEBHOOK`, and `EASYPANEL_N8N_DEPLOY_WEBHOOK`.
- Call `curl -fsS -X POST "$WEBHOOK"` inside a step guarded by the matching boolean input.

This approach creates a clear chain: quality gate passes → deploy workflow runs → webhook fires → Easypanel redeploys the service.

If the team prefers simplicity and `main` is already protected by required checks, Easypanel Auto Deploy is also valid. In that mode, Easypanel creates the webhook in the GitHub repository and deploys on every push. You trade the explicit pipeline gate for less workflow code.

## Supabase migrations in deploy

Before firing app webhooks, apply database migrations when `deploy_supabase` is true:

```yaml
supabase link --project-ref "$SUPABASE_PROJECT_ID" --password "$SUPABASE_DB_PASSWORD"
supabase db push --linked --password "$SUPABASE_DB_PASSWORD"
```

Use environment-scoped secrets for `SUPABASE_ACCESS_TOKEN` and `SUPABASE_DB_PASSWORD`, and environment variables for `SUPABASE_PROJECT_ID`.

## Smoke tests

After triggering webhooks, wait briefly for the service to roll out, then run lightweight HTTP smoke tests:

- Web: `curl -fsS --retry 10 --retry-delay 10 "$WEB_SMOKE_URL"`
- API: `curl -fsS --retry 10 --retry-delay 10 "$API_SMOKE_URL"`
- n8n: hit the readiness endpoint, for example `/healthz/readiness`, not just the editor root.

Store smoke URLs as environment variables (`vars`), not secrets, because they are not sensitive.

## Notifications

Add a `notify-failure` job that depends on the quality gate or deploy job and runs `if: failure() && !cancelled()`. Post a short message to Slack or Discord using webhook secrets. Include the run URL so the team can investigate quickly.

Read notification snippets in [`references/deploy-yml-template.md`](references/deploy-yml-template.md).

## Concurrency and cost control

- In CI, use `concurrency: { group: ci-${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` to cancel stale builds on active branches.
- In deploy, do not set `cancel-in-progress: true`; use a queue so deployments finish in order.

## Secrets and governance

Prefer GitHub Environment secrets and variables over repository-level secrets when values differ between staging and production.

Read the full checklist in [`references/secrets-checklist.md`](references/secrets-checklist.md).

Key rules:

- Keep webhook URLs, database passwords, and access tokens as environment secrets.
- Keep project IDs and smoke URLs as environment variables.
- Reference secrets explicitly; GitHub only injects a secret when it is used.
- Pass secrets to reusable workflows with `secrets: inherit` or map them explicitly.
- Protect `.github/workflows` changes with CODEOWNERS or required review.
- Pin actions by full SHA in security-sensitive repositories.

## Common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| PR check stuck on "Pending" | Workflow skipped by `paths` filter while required | Run workflow always; filter inside jobs |
| Lint never runs in Next.js | Assuming `next build` runs lint | Add explicit ESLint CLI step |
| Secret unavailable in reusable workflow | Missing `secrets: inherit` | Pass secrets explicitly |
| `supabase db push` auth fails | Missing or wrong `SUPABASE_DB_PASSWORD` | Use password-based link/push and check IP allowlists |
| Docker build succeeds but container not runnable | Missing `load: true` in build-push-action | Add `load: true` when you need local image |
| n8n smoke test passes but service is not ready | Hitting editor root instead of readiness | Use `/healthz/readiness` |

Read more troubleshooting guidance in [`references/troubleshooting.md`](references/troubleshooting.md).

## Skill references

- [`references/ci-yml-template.md`](references/ci-yml-template.md) — Complete `ci.yml` template with change detection, parallel jobs, quality gate, and deploy call.
- [`references/deploy-yml-template.md`](references/deploy-yml-template.md) — Reusable `deploy.yml` template with Easypanel webhooks, Supabase migrations, smoke tests, and notifications.
- [`references/secrets-checklist.md`](references/secrets-checklist.md) — Environment secrets, variables, and governance rules.
- [`references/troubleshooting.md`](references/troubleshooting.md) — Common failures and fixes.
- [`references/easypanel-deploy-skill-link.md`](references/easypanel-deploy-skill-link.md) — Pointer to the Easypanel deploy skill for host setup, Dockerfiles, and service configuration.
