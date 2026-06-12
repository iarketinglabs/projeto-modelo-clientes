# Ferramentas e comandos de scan

Um pipeline de auditoria minimamente profissional para o stack Atomica deve cobrir dependências, código, segredos, imagens/containers, SBOM e, quando houver IaC, configuração.

## Dependências e vulnerabilidades conhecidas

```bash
# JavaScript / Node
npm audit --json

# Python
pip-audit -r requirements.txt

# OSV para múltiplos ecossistemas
osv-scanner scan .
```

- `npm audit` consulta vulnerabilidades conhecidas a partir das dependências do projeto.
- `pip-audit` verifica ambientes ou requirements Python contra advisories conhecidos.
- `osv-scanner` conecta manifests e lockfiles à base OSV, com saída HTML e guided remediation em cenários compatíveis.

## Imagens, filesystem e SBOM

```bash
# Scan de filesystem/projeto
trivy fs .

# Scan de imagem container
trivy image ghcr.io/sua-org/seu-app:latest

# Gerar SBOM
syft dir:. -o cyclonedx-json > sbom.json

# Scan a partir do SBOM
grype sbom:sbom.json
```

- `Trivy` — scanner open-source amplo para vulnerabilidades, IaC e cloud-native security.
- `Syft` — gera SBOM em formatos como CycloneDX/SPDX.
- `Grype` — lê imagem, filesystem ou SBOM para vulnerabilidades conhecidas.

## Código e segredos

```bash
# SAST local com regras padrão
semgrep scan --config "p/default"

# Segredos em diretórios
gitleaks dir -v .

# Segredos no histórico git
gitleaks git
```

- `Semgrep` permite scan local de segurança sem exigir conta.
- `Gitleaks` detecta credenciais em arquivos e no histórico Git.

Adicione regras internas para detectar:

- `SUPABASE_SERVICE_ROLE_KEY` em código cliente ou `.env.example`.
- Tokens de provedores de IA hardcoded.
- `N8N_ENCRYPTION_KEY` em lugar errado.
- Segredos em notebooks e scripts auxiliares.

## Complemento opcional

```bash
# Ferramenta popular, mas comercial/freemium
snyk test
```

Snyk funciona bem como camada adicional de priorização e remediação, mas não como peça única da estratégia.

## Critério de aceite para CI

Falhe a build quando:

- Segredo exposto for detectado.
- Service key privilegiada for usada em código cliente.
- CVE crítico não tiver justificativa formal.
- Tabela expusa não tiver RLS.
- Webhook de produção não tiver autenticação.
- Release candidate não incluir SBOM.

Essa tradução operacional une OWASP 2025, higiene de supply chain, least privilege e accountability.
