# SBOM Commands Reference

## Node.js / Next.js

### npm sbom

```bash
# SPDX 2.3 from lockfile
npm sbom --sbom-format spdx --package-lock-only > sbom.node.spdx.json

# CycloneDX 1.5 from lockfile
npm sbom --sbom-format cyclonedx --package-lock-only > sbom.node.cdx.json

# Production dependencies only
npm sbom --sbom-format cyclonedx --package-lock-only --omit dev > sbom.node.prod.cdx.json

# Single workspace
npm sbom --sbom-format spdx --workspace packages/api > sbom.api.spdx.json

# All workspaces
npm sbom --sbom-format spdx --workspaces > sbom.monorepo.spdx.json
```

### Syft on Node repo

```bash
syft scan . \
  -o spdx-json@2.3=sbom.repo.spdx.json \
  -o cyclonedx-json@1.5=sbom.repo.cdx.json
```

## Python

### Resolve without installing

```bash
python -m pip install --dry-run --ignore-installed -r requirements.txt --report pip-report.json
```

### Resolve in a clean virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip inspect > pip-inspect.json
```

For `pyproject.toml` projects, replace the install step with:

```bash
python -m pip install .
```

### Syft on resolved environment

```bash
syft scan .venv \
  -o spdx-json@2.3=sbom.python.spdx.json \
  -o cyclonedx-json@1.5=sbom.python.cdx.json
```

### cdxgen enrichment

```bash
# Requires Java >= 21 for Python/C projects
cdxgen -o sbom.python.cdx.json --spec-version 1.5 .
```

## Docker

### Build and scan with Syft

```bash
docker build -t myapp:${GIT_SHA:-local} .

syft scan myapp:${GIT_SHA:-local} \
  -o spdx-json@2.3=sbom.image.spdx.json \
  -o cyclonedx-json@1.5=sbom.image.cdx.json
```

### Scan with Trivy

```bash
trivy image --format spdx-json --output sbom.image.trivy.spdx.json myapp:${GIT_SHA:-local}
trivy image --format cyclonedx --output sbom.image.trivy.cdx.json myapp:${GIT_SHA:-local}
```

To include vulnerabilities in the CycloneDX output:

```bash
trivy image --format cyclonedx --scanners vuln --output sbom.image.vuln.cdx.json myapp:${GIT_SHA:-local}
```

## GitHub REST API export

Export the dependency graph SBOM that GitHub already sees:

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  https://api.github.com/repos/OWNER/REPO/dependency-graph/sbom
```

This returns SPDX 2.3 JSON, but it is conceptually a repository dependency graph, not an image SBOM.
