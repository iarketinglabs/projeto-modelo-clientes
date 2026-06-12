# SBOM Tool Comparison

| Tool | Useful formats for Atomica | Installation | Strengths | Limitations | Best use |
|---|---|---|---|---|---|
| **npm sbom** | SPDX 2.3, CycloneDX 1.5 | Bundled with npm | Fast path for Node.js; supports `--package-lock-only`, `--omit`, `--workspace`, `--workspaces` | npm-only; no Python or Docker | Node.js/Next.js app-level SBOM from lockfile |
| **Syft** | SPDX 2.3, CycloneDX 1.5 with explicit schema pin | `curl -sSfL https://get.anchore.io/syft \| sudo sh -s -- -b /usr/local/bin` | Multi-ecosystem; scans directories, images, files, OCI layouts; pins schema versions | Open-standard export may reduce/transform native Syft metadata | Primary generator for polyglot repos and Docker images |
| **Trivy** | SPDX, CycloneDX | Script, package, container, or action | Scans fs, image, rootfs; mature GitHub Action; submits snapshots to GitHub dependency graph; also scans licenses and vulnerabilities | `--format cyclonedx` disables vulnerability scan by default; reanalysis of third-party SBOMs may lose precision | Unified SBOM + security + GitHub integration |
| **cdxgen** | CycloneDX 1.5–1.7; SPDX 3.0.1 JSON-LD (not 2.3) | `npm install -g @cyclonedx/cdxgen` or container | Excellent CycloneDX output; retains dependency trees; application/services modeling; server mode | Requires Java >= 21 for Python/C flows; default spec is 1.7, so pin `--spec-version 1.5` | CycloneDX enrichment, app-level BOM, server/API use |
| **spdx-sbom-generator** | SPDX 2.2 | Binaries, Homebrew, Scoop | Historical SPDX ecosystem tool | Archived/deprecated since 2025; stuck on SPDX 2.2 | Avoid for greenfield; only for specific legacy needs |

## Bottom line

- If you need one tool that covers the required formats and stacks, choose **Syft**.
- If you want to couple SBOM generation with vulnerability scanning and GitHub dependency graph submission, add **Trivy**.
- If you want richer CycloneDX modeling at the application/services level, add **cdxgen** as a complement, not a replacement for the SPDX 2.3 generator.
