# Security Policy

## Supported versions

Security fixes are provided for the latest public release on the default branch. Older snapshots may no longer receive fixes.

## Reporting a vulnerability

Do not open a public issue for vulnerabilities or include credentials, tokens, account exports, request logs or database files in a report.

Use the repository's **Security > Advisories > Report a vulnerability** flow when available. If private advisories are unavailable, contact the repository maintainer through the private contact method listed on their GitHub profile and request a private reporting channel.

Please include:

- Affected version or commit
- Deployment mode, such as local, LAN, Docker or reverse proxy
- Reproduction steps with secrets removed
- Security impact and proposed mitigation
- Whether the issue has been disclosed elsewhere

## Secrets and data

The repository must not contain:

- OAuth access or refresh tokens
- API keys or panel passwords
- Account exports or user identifiers
- Usage databases, request logs or backups
- Private keys, session cookies or <code>.env</code> files

Run <code>python3 scripts/check_release.py</code> before every release. A scan failure should block publication.

## Secure deployment baseline

- Run behind an HTTPS reverse proxy for any non-local deployment
- Bind to <code>127.0.0.1</code> unless LAN access is required
- Set a unique panel password at first start
- Restrict network access with a firewall or private network
- Rotate API keys after suspected disclosure
- Keep Python, the base image and reverse proxy patched
- Back up encrypted data separately from source releases

## Scope

The project does not control upstream services or their security. Report vulnerabilities in upstream services to the appropriate service operator.
