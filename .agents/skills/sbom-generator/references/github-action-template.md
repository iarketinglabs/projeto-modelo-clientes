# GitHub Actions Templates

## Full SBOM generation workflow

This workflow generates repository and image SBOMs on every push, pull request, and manual dispatch.

```yaml
name: sbom

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  generate-sbom:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Install Syft
        run: curl -sSfL https://get.anchore.io/syft | sudo sh -s -- -b /usr/local/bin

      - name: Generate repository SBOMs
        run: |
          syft scan . \
            -o spdx-json@2.3=sbom.repo.spdx.json \
            -o cyclonedx-json@1.5=sbom.repo.cdx.json

      - name: Build image
        run: docker build -t app:${{ github.sha }} .

      - name: Generate image SBOMs
        run: |
          syft scan app:${{ github.sha }} \
            -o spdx-json@2.3=sbom.image.spdx.json \
            -o cyclonedx-json@1.5=sbom.image.cdx.json

      - name: Upload SBOM artifacts
        uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ github.sha }}
          path: |
            sbom.repo.spdx.json
            sbom.repo.cdx.json
            sbom.image.spdx.json
            sbom.image.cdx.json
          retention-days: 30
```

## Submit dependency snapshot to GitHub

Use this separate job only if you want to populate the GitHub dependency graph. It requires write permission on `contents`.

```yaml
permissions:
  contents: write

jobs:
  submit-dependency-snapshot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Submit dependency snapshot to GitHub
        uses: aquasecurity/trivy-action@v0.36.0
        with:
          scan-type: fs
          scan-ref: .
          format: github
          output: dependency-results.sbom.json
          github-pat: ${{ secrets.GITHUB_TOKEN }}
```

## Notes

- Fix the Syft installer URL and Trivy Action version to a known release in production workflows.
- Use `retention-days` to control artifact storage costs.
- Keep the SBOM generation job on `contents: read` unless dependency-graph submission is required.
