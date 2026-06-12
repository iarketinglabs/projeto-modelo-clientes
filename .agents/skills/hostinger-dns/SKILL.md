---
name: hostinger-dns
description: Configure Hostinger DNS to point domains and subdomains to an Easypanel instance, handle SSL, redirects, and propagation validation. Use this skill whenever the user mentions Hostinger DNS, domain configuration, DNS records, A/CNAME/CAA/ALIAS/MX/TXT records, SSL setup, www or http→https redirects, Easypanel domain setup, or pointing a Hostinger-managed domain to a VPS running Easypanel.
---

# Hostinger DNS for Easypanel

This skill guides the setup of Hostinger DNS when the application runs on a VPS with Easypanel. The goal is to keep Hostinger as the authoritative DNS zone, point hostnames to the VPS public IP, and let Easypanel terminate HTTPS and route traffic by hostname.

## When to use this skill

Use this skill for:

- Pointing a Hostinger-managed domain or subdomain to an Easypanel VPS.
- Choosing between A, CNAME, CAA, ALIAS, MX, and TXT records.
- Setting up SSL/Let's Encrypt certificates for Easypanel apps.
- Configuring www → apex and HTTP → HTTPS redirects.
- Validating DNS propagation and troubleshooting resolution or certificate issues.

## Reference architecture

The recommended layout keeps Hostinger as the DNS authority and Easypanel as the HTTPS/proxy termination point:

- Hostinger DNS Zone Editor holds the zone records.
- The apex domain (`@`) points to the VPS public IPv4 via an A record.
- Subdomains (`www`, `app`, `api`, `admin`) point to the same IP or to the apex domain as appropriate.
- Easypanel receives the traffic on ports 80/443 and routes each hostname to the correct app service via Domains & Proxy.
- Redirects (www → non-www, HTTP → HTTPS) are HTTP-layer concerns handled by Hostinger Redirects, Traefik, or the app, not by DNS records.

Before editing any records, confirm who is authoritative for the domain. If the nameservers are not Hostinger's, edit the zone at the current authoritative provider, not in hPanel.

## Step-by-step workflow

1. **Confirm DNS authority.** Run `dig NS dominio.tld +short` or a WHOIS lookup. If the nameservers belong to Hostinger, proceed in hPanel. Otherwise, manage the zone where the NS records point.
2. **Open Hostinger DNS Zone Editor.** Remove stale or conflicting A/AAAA/CNAME records for the hosts you are about to configure. Conflicting records cause partial or broken resolution.
3. **Create the apex A record.** Point `@` to the public IPv4 of the Easypanel VPS. Use the default TTL of `14400` seconds unless the project needs something different.
4. **Create subdomains.** For `www`, prefer a CNAME to the apex domain. For `app`, `api`, `admin`, or other project hostnames, use A records to the same VPS IP when they are served by the same Easypanel/Traefik instance.
5. **Preserve email records.** Do not delete or overwrite MX, SPF, DKIM, or DMARC TXT records unless the email provider is also changing.
6. **Configure Easypanel Domains & Proxy.** Add each hostname to the correct app service and set the internal proxy port to the port the app listens on (for example, `3000`, `8000`).
7. **Open ports 80 and 443.** Ensure the VPS firewall and any cloud security group allow inbound HTTP and HTTPS traffic. Easypanel needs these ports for web serving and Let's Encrypt validation.
8. **Validate and wait.** Check authoritative resolution first, then public resolver propagation. DNS changes can take minutes to hours depending on TTL and cache state.

## Record types

See `references/typical-records.md` for a complete table and placeholder examples.

- **A**: Maps a host to an IPv4 address. Use for `@`, `app`, `api`, `admin` when the destination is the VPS IP.
- **CNAME**: Maps a host to another hostname. Use for `www` pointing to the apex domain. Do not use CNAME on the apex if MX or TXT records must coexist; use ALIAS instead.
- **ALIAS**: Flattens an apex domain to a target hostname without breaking MX/TXT. Use when the root domain must point to a hostname rather than an IP.
- **CAA**: Restricts which certificate authorities may issue certificates. Optional; add only if the project has a CA policy.
- **MX/TXT**: Required for email routing and authentication. Preserve existing records during web changes.

## SSL and redirects

- **Standard domain/subdomain certificates**: Let Easypanel issue them automatically via HTTP-01. Port 80 must be reachable from the internet, and the hostname must resolve to the VPS.
- **Wildcard certificates**: Require DNS-01 challenge. This needs a Traefik certificate resolver configured with an ACME DNS provider that can update Hostinger DNS, such as the Lego `hostinger` provider. Treat wildcard automation as an advanced path that should be tested in staging first.
- **Redirects**: Keep DNS and HTTP layers separate. DNS resolves names; redirects are HTTP behavior.
  - Use Hostinger Redirects for simple whole-domain forwarding.
  - Use Traefik middleware (`RedirectScheme`, `RedirectRegex`) or the app itself for canonical www → apex and HTTP → HTTPS redirects that preserve paths.

## Propagation validation

Validate first against the authoritative nameserver, then against public resolvers. This separates zone issues from cache issues.

See `references/validation-commands.md` for ready-to-run `dig`, `nslookup`, and `curl` commands.

Quick checks:

```bash
# authoritative nameserver
dig NS dominio.tld +short
dig A dominio.tld @ns1.dns-parking.com +short

# public resolution
dig A dominio.tld +short
dig CNAME www.dominio.tld +short
nslookup dominio.tld 8.8.8.8

# HTTP/S and redirects
curl -I http://dominio.tld
curl -I http://www.dominio.tld
curl -I https://dominio.tld
```

## Checklist

Use `references/checklist.md` for the full post-configuration checklist. The most important items are:

- Apex A record resolves to the correct VPS IP on the authoritative server.
- Each hostname is added to Easypanel Domains & Proxy with the correct internal port.
- Ports 80 and 443 are open on the server and firewall.
- Redirects behave as expected when tested with `curl -I`.
- MX, SPF, DKIM, and DMARC records remain intact.

## Troubleshooting

See `references/troubleshooting.md` for detailed symptom/cause/fix guidance. Common issues include:

- Editing the Hostinger zone when the domain is delegated to external nameservers.
- Stale A/AAAA records conflicting with new entries.
- SSL failing because port 80 is closed or the proxy port is misconfigured.
- Mixed content warnings after switching to HTTPS.
- DNS propagation delays mistaken for misconfiguration.

## Limits and advanced paths

- **Wildcard DNS-01 automation** with Hostinger DNS is theoretically supported through Traefik/Lego, but the exact Easypanel UI fields for the Hostinger provider are not documented in the researched material. Test in a non-production environment first.
- **HTTP → HTTPS forcing** is not guaranteed to be enabled by default in every Easypanel scenario. Verify with `curl -I` and apply a redirect middleware if needed.
