# Troubleshooting Hostinger DNS → Easypanel issues

## Domain resolves to the wrong place or does not resolve

**Likely causes**

1. The zone is being edited in Hostinger, but the domain delegates to external nameservers. Use `dig NS dominio.tld +short` to confirm authority.
2. Stale A or AAAA records conflict with the new entries. Clean up old records in the DNS Zone Editor.
3. DNS propagation is still in progress. Authoritative servers may already be correct while public caches still hold old values.
4. Residual DNSSEC from a previous nameserver change is breaking validation. Hostinger-managed zones using Hostinger nameservers do not support DNSSEC.

**What to do**

- Confirm authoritative nameservers before editing.
- Remove conflicting A/AAAA records.
- Query authoritative servers directly, then public resolvers, to separate zone issues from cache.
- Disable or update DNSSEC if the delegation recently changed.

## SSL certificate does not issue in Easypanel

**Likely causes**

- Hostname does not yet resolve to the VPS public IP.
- Port 80 is blocked on the server or firewall.
- Easypanel proxy port is set to a port the app is not listening on.
- Wildcard certificate requested with HTTP-01 challenge instead of DNS-01.
- CAA record restricts issuance to a different certificate authority.

**What to do**

- Verify A record resolution against the authoritative server.
- Open ports 80 and 443 inbound.
- Confirm the app's listening port matches the Easypanel proxy port.
- Use DNS-01 for wildcard certificates; confirm `letsencrypt.org` is allowed in CAA if CAA exists.

## Site loads as "not secure" on some pages

**Likely cause**: Mixed content. The page is served over HTTPS, but some assets (images, CSS, JS, fonts) still use `http://`.

**What to do**

- Update asset URLs to `https://` in code, theme, config, or database.
- Consider `upgrade-insecure-requests` as a temporary policy while fixing source URLs.

## `www` works but apex does not, or vice versa

**Likely causes**

- Missing A or CNAME record for one of the hosts.
- Canonical redirect is not configured after both hosts resolve.

**What to do**

- Ensure both hosts have valid DNS records.
- Add the redirect (www → apex or apex → www) in Hostinger Redirects, Traefik, or the app.

## Some regions see the new IP and others do not

**Likely cause**: Recursive resolver cache. Each resolver honors the record's TTL before refreshing.

**What to do**

- Verify the authoritative server already has the correct value.
- Wait for the TTL to expire on public resolvers.
- Use multiple geographic resolvers or propagation checkers to monitor progress.
