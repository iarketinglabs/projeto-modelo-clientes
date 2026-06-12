# NTIA Minimum Elements Checklist

The NTIA *Minimum Elements for an SBOM* covers three areas: Data Fields, Automation Support, and Practices and Processes.

## Required data fields

| NTIA field | Required | Practical guidance |
|---|---|---|
| Supplier name | Yes | Use the organization that produces or delivers the software. |
| Component name | Yes | Name of the application, service, package, or primary image. |
| Version of the component | Yes | Release version, tag, commit SHA, or image digest. |
| Other unique identifiers | Yes | Prefer purl, checksums, image digest, and download locations. |
| Dependency relationship | Yes | Include the dependency graph; avoid flat package lists. |
| Author of SBOM data | Yes | Record the toolchain or person that generated the document. |
| Timestamp | Yes | Use UTC generation time. |

## Strongly recommended additions

| Field | Guidance |
|---|---|
| License | Not an NTIA minimum, but include it because most compliance workflows expect it. SPDX and CycloneDX both support license metadata natively. |
| Supplier contact | Useful for procurement and audit follow-up. |
| Known vulnerabilities | VEX or VDR attachments when the SBOM is used for security workflows. |

## Format compliance

- SPDX 2.3 JSON and CycloneDX 1.5 JSON both satisfy NTIA automation-support requirements.
- Deliver both formats when the client requests maximum transparency.
- Pin the schema version explicitly in generation commands to avoid downstream surprises.
