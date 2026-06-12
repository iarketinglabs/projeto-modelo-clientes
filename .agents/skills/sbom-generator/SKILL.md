---
name: sbom-generator
description: Generate Software Bill of Materials (SBOM) artifacts in SPDX 2.3 and CycloneDX 1.5 for Node.js, Python, and Docker projects. Use this skill whenever the user mentions SBOM, SPDX, CycloneDX, dependency inventory, software bill of materials, supply chain security, dependency graph export, or vulnerability traceability. Covers tool selection (Syft, Trivy, npm sbom, cdxgen), deterministic generation from lockfiles and resolved environments, image scanning, GitHub Actions integration, and client-ready delivery packaging.
---

# SBOM Generator

Generate SBOM artifacts for Atomica projects in SPDX 2.3 and CycloneDX 1.5. This skill targets Node.js/Next.js, Python, and Docker artifacts, and emphasizes reproducible, auditable deliveries.

## SPDX vs CycloneDX

Pick the format based on what the SBOM must prove:

- **SPDX 2.3** — Prefer for compliance, procurement, contracts, and GitHub dependency-graph exports. It is an ISO/IEC 5962:2021 standard and the format GitHub uses for REST API exports.
- **CycloneDX 1.5** — Prefer for operational security, dependency graphs, services modeling, and VEX/VDR workflows. Its `services` element fits external dependencies like Supabase better than a flat package list.

When a client asks for maximum transparency, deliver both: `sbom.spdx.json` + `sbom.cdx.json`. They are complementary, not interchangeable.

## High-level workflow

1. Identify the target: source repository, built application, or container image.
2. Resolve dependencies deterministically before generating:
   - Node.js: rely on `package-lock.json`.
   - Python: resolve in a clean virtual environment or use `pip --report`; do not generate from raw `requirements.txt` alone.
   - Docker: build the image first, then scan the image.
3. Choose the tool (see `references/tool-comparison.md`).
4. Generate both SPDX 2.3 and CycloneDX 1.5 with pinned schema versions.
5. Validate the output contains supplier, component name, version, identifiers, dependency graph, author, and timestamp.
6. Package the delivery with metadata, checksums, and generation commands (see `references/delivery-template.md`).

## Tool selection

The default generator is **Syft** because it pins `spdx-json@2.3` and `cyclonedx-json@1.5` explicitly and covers directories, images, and OCI layouts.

Use the right tool for the job:

- **Syft** — Primary generator for polyglot repos and Docker images.
- **npm sbom** — Fast path for Node.js/Next.js when `package-lock.json` is trustworthy.
- **Trivy** — Use when SBOM generation is part of a unified security/GitHub Actions workflow.
- **cdxgen** — Use as a CycloneDX enricher for application-level BOMs; do not use it as the only SPDX 2.3 generator.

For the full comparison, read `references/tool-comparison.md`.

## Commands by stack

### Node.js / Next.js

Generate from the lockfile for a deterministic application-level SBOM:

```bash
# SPDX 2.3
npm sbom --sbom-format spdx --package-lock-only > sbom.node.spdx.json

# CycloneDX 1.5
npm sbom --sbom-format cyclonedx --package-lock-only > sbom.node.cdx.json

# Production scope only
npm sbom --sbom-format cyclonedx --package-lock-only --omit dev > sbom.node.prod.cdx.json

# Monorepo
npm sbom --sbom-format spdx --workspaces > sbom.monorepo.spdx.json
```

For a single command that also covers any Python files in the same repo:

```bash
syft scan . \
  -o spdx-json@2.3=sbom.repo.spdx.json \
  -o cyclonedx-json@1.5=sbom.repo.cdx.json
```

### Python

Avoid generating from an unresolved manifest. Resolve first, then scan.

Option A — resolve without installing:

```bash
python -m pip install --dry-run --ignore-installed -r requirements.txt --report pip-report.json
```

Option B — resolve in a clean virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip inspect > pip-inspect.json
syft scan .venv \
  -o spdx-json@2.3=sbom.python.spdx.json \
  -o cyclonedx-json@1.5=sbom.python.cdx.json
```

For a richer CycloneDX output, add cdxgen pinned to 1.5:

```bash
cdxgen -o sbom.python.cdx.json --spec-version 1.5 .
```

### Docker

Always generate the SBOM from the built image, not just the repo:

```bash
docker build -t myapp:${GIT_SHA:-local} .

syft scan myapp:${GIT_SHA:-local} \
  -o spdx-json@2.3=sbom.image.spdx.json \
  -o cyclonedx-json@1.5=sbom.image.cdx.json
```

Trivy alternative:

```bash
trivy image --format spdx-json --output sbom.image.trivy.spdx.json myapp:${GIT_SHA:-local}
trivy image --format cyclonedx --output sbom.image.trivy.cdx.json myapp:${GIT_SHA:-local}
```

For the full command reference, read `references/commands.md`.

## GitHub Actions integration

Add an `sbom` workflow that:

1. Checks out the repository.
2. Installs Syft.
3. Generates repository SBOMs.
4. Builds the Docker image.
5. Generates image SBOMs.
6. Uploads all files as versioned artifacts.

If you also want to submit dependency snapshots to the GitHub dependency graph, use the Trivy Action with `format: github` and `contents: write` permission.

For ready-to-use workflow templates, read `references/github-action-template.md`.

## Delivery package

A client delivery is not a single JSON file. Bundle it as:

```
sbom-delivery/
├── README.md
├── source/
│   ├── sbom.repo.spdx.json
│   └── sbom.repo.cdx.json
├── image/
│   ├── sbom.image.spdx.json
│   └── sbom.image.cdx.json
├── metadata/
│   ├── checksums.txt
│   ├── generation-commands.txt
│   └── tool-versions.txt
└── optional/
    ├── dependency-results.sbom.json
    └── attestation-or-signature
```

The README should state supplier, product, release, commit, image digest, formats delivered, lifecycle phases, scope, exclusions, tools used, timestamps, and exact commands.

For a complete delivery template, read `references/delivery-template.md`.

## Quality checklist

Before calling an SBOM delivery complete, verify it covers the NTIA minimum elements:

- Supplier name
- Component name
- Component version
- Other unique identifiers (purl, checksums, image digest)
- Dependency relationship (graph, not a flat list)
- Author of SBOM data
- Timestamp (UTC)

License information is not an NTIA minimum, but include it anyway because most compliance workflows expect it.

For the full checklist mapped to SPDX/CycloneDX fields, read `references/ntia-checklist.md`.

## Common pitfalls

- **Python manifest-only SBOMs** — `requirements.txt` and `pyproject.toml` declare install requests, not a resolved tree. Generate from a resolved environment or `pip --report`.
- **Default schema versions** — Syft, cdxgen, and Trivy defaults change over time. Pin `spdx-json@2.3` and `cyclonedx-json@1.5` explicitly.
- **cdxgen for SPDX 2.3** — cdxgen exports SPDX 3.0.1 JSON-LD, not SPDX 2.3. Use Syft or Trivy for SPDX 2.3.
- **GitHub Actions defaults** — Some community actions still emit SPDX 2.2. Generate with Syft/Trivy/npm directly when 2.3 is required.
- **Repo SBOM vs image SBOM** — The repository SBOM captures declared dependencies; the image SBOM captures what actually ships, including OS packages and copied binaries. Deliver both when releasing Docker artifacts.
