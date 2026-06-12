# Post-configuration checklist for Hostinger DNS → Easypanel

Use this checklist after changing DNS records or publishing a new app hostname.

## DNS records

- [ ] Confirmed Hostinger is the authoritative DNS provider with `dig NS dominio.tld +short`.
- [ ] Removed stale or conflicting A/AAAA/CNAME records for the hosts being configured.
- [ ] Created apex A record `@` pointing to the VPS public IPv4.
- [ ] Created `www` as CNAME to the apex domain, or as an A record if required by the project.
- [ ] Created `app`, `api`, `admin`, or other project subdomains as A records to the VPS IP.
- [ ] Preserved MX, SPF, DKIM, DMARC, and any verification TXT records.
- [ ] Added CAA records only if the project enforces a specific certificate authority policy.

## Easypanel

- [ ] Added each hostname to the correct app service under Domains & Proxy.
- [ ] Set the internal proxy port to the port the app actually listens on.
- [ ] Confirmed ports 80 and 443 are open on the VPS firewall and cloud security group.
- [ ] Confirmed SSL certificate was issued successfully by Easypanel/Let's Encrypt.

## Validation

- [ ] Authoritative nameserver returns the correct A record values.
- [ ] Public resolvers (8.8.8.8, 1.1.1.1) return the expected values or show propagation in progress.
- [ ] `curl -I http://dominio.tld` behaves as planned for HTTP → HTTPS redirects.
- [ ] `curl -I http://www.dominio.tld` behaves as planned for www → apex redirects.
- [ ] `curl -I https://dominio.tld` returns `200 OK` with a valid certificate.
- [ ] No mixed-content warnings in the browser; all assets load over HTTPS.

## Timing

- [ ] Allowed up to the TTL window (default 14400 seconds / 4 hours) for recursive caches to expire.
- [ ] Allowed up to 24 hours for full global propagation; up to 48 hours after nameserver changes.
