# Typical DNS records for an Atomica + Easypanel project

This table assumes a single VPS running Easypanel, with Hostinger as the authoritative DNS provider and multiple hostnames served by the same Traefik/Easypanel proxy.

| Type  | Host    | Value                         | TTL   | Recommended use |
|-------|---------|-------------------------------|-------|-----------------|
| A     | `@`     | `<VPS_PUBLIC_IP>`             | 14400 | Apex domain pointing to the Easypanel VPS |
| CNAME | `www`   | `<PRIMARY_DOMAIN>`            | 14400 | `www` resolving to the apex domain |
| A     | `app`   | `<VPS_PUBLIC_IP>`             | 14400 | Main application |
| A     | `api`   | `<VPS_PUBLIC_IP>`             | 14400 | API served by the same proxy |
| A     | `admin` | `<VPS_PUBLIC_IP>`             | 14400 | Admin panel |
| CAA   | `@`     | `issue "letsencrypt.org"`     | 14400 | Optional: restricts issuing CA for standard certs |
| CAA   | `@`     | `issuewild "letsencrypt.org"` | 14400 | Optional: only useful if using DNS-01 wildcard certs |
| ALIAS | `@`     | `<TARGET_HOSTNAME>`           | 14400 | Use instead of A on apex when the target is a hostname, not an IP |
| MX    | varies  | `<KEEP_PER_EMAIL_PROVIDER>`   | as-is | Preserve existing email routing |
| TXT   | varies  | `<SPF/DKIM/DMARC/VERIFICATION>` | as-is | Preserve email auth and verification records |

## Notes

- Replace `<VPS_PUBLIC_IP>` with the actual public IPv4 of the Easypanel server.
- Replace `<PRIMARY_DOMAIN>` with the registered domain, for example `example.com`.
- Use ALIAS on the apex only when the destination must be a hostname. CNAME on the apex breaks coexistence with MX and TXT records.
- Keep MX and TXT records intact unless the project's email provider is also changing.
- The default TTL of `14400` seconds (4 hours) is the value commonly documented by Hostinger for these record types.
