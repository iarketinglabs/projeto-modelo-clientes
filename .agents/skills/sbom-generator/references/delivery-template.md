# SBOM Delivery Template

## Package structure

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

## README.md template

```markdown
# SBOM Delivery

## Supplier
Atomica

## Product
Nome do sistema / serviço

## Release
vX.Y.Z

## Commit
<git-sha>

## Container image
ghcr.io/org/app@sha256:<digest>

## Formats delivered
- SPDX 2.3 JSON
- CycloneDX 1.5 JSON

## Lifecycle phase
- Source/repository
- Built container image

## Scope
- Node.js / Next.js dependencies
- Python dependencies
- Docker image contents

## Exclusions
- External SaaS services not inferred automatically by the generator
- Local development tools outside the final artifact

## Generation tools
- Syft v...
- Trivy v...
- npm v...

## Generation timestamps
- source: 2026-06-10T...Z
- image: 2026-06-10T...Z

## Commands used
<paste exact commands here>

## Notes
- License field included for compliance convenience.
- Repository SBOM and image SBOM are complementary, not interchangeable.
```

## metadata/checksums.txt template

```
sha256  sbom.repo.spdx.json  <hash>
sha256  sbom.repo.cdx.json   <hash>
sha256  sbom.image.spdx.json <hash>
sha256  sbom.image.cdx.json  <hash>
```

## metadata/generation-commands.txt template

```bash
# Repository SBOMs
syft scan . -o spdx-json@2.3=sbom.repo.spdx.json -o cyclonedx-json@1.5=sbom.repo.cdx.json

# Image SBOMs
docker build -t app:<sha> .
syft scan app:<sha> -o spdx-json@2.3=sbom.image.spdx.json -o cyclonedx-json@1.5=sbom.image.cdx.json
```

## metadata/tool-versions.txt template

```
Syft v1.2.3
Trivy v0.54.0
npm v10.8.0
cdxgen v10.0.0
```
