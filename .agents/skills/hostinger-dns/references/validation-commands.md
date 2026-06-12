# DNS propagation and HTTPS validation commands

Run these commands to separate authoritative zone state from public resolver cache.

## Identify authoritative nameservers

```bash
dig NS dominio.tld +short
whois dominio.tld | grep -i "name server"
```

## Query the authoritative server directly

Replace `ns1.dns-parking.com` with the actual authoritative nameserver returned above.

```bash
dig A dominio.tld @ns1.dns-parking.com +short
dig A app.dominio.tld @ns1.dns-parking.com +short
dig A api.dominio.tld @ns1.dns-parking.com +short
dig CNAME www.dominio.tld @ns1.dns-parking.com +short
```

## Query public resolvers

```bash
dig A dominio.tld +short
dig A app.dominio.tld +short
dig A api.dominio.tld +short
dig CNAME www.dominio.tld +short

nslookup dominio.tld 8.8.8.8
nslookup dominio.tld 1.1.1.1
```

## Validate redirects and HTTPS

```bash
# Check apex HTTP behavior
curl -I http://dominio.tld

# Check www behavior
curl -I http://www.dominio.tld

# Check HTTPS availability
curl -I https://dominio.tld
curl -I https://app.dominio.tld
```

## Expected results

- `dig A` should return the VPS public IP.
- `dig CNAME www` should return the apex domain.
- `curl -I http://dominio.tld` should return `301` or `302` if forcing HTTPS or canonical host.
- `curl -I https://dominio.tld` should return `200 OK` and no certificate errors.
