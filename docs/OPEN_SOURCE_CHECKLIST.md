# Open source publication checklist

## Completed in this repository

- MIT license and upstream attribution
- Non-affiliation and trademark notice
- README, architecture, deployment and security documentation
- Contributor guide and code of conduct
- Issue forms and pull request template
- Python compile, smoke test and release safety checks
- CI for Python 3.11, 3.12 and 3.13
- Docker build check in CI
- Tag-based source release workflow
- Runtime data and credential exclusions

## Before creating the remote repository

1. Choose the final GitHub owner and repository name.
2. Confirm that you have the right to redistribute every source file and that your use complies with the upstream service terms and local law.
3. Rotate any deployment API keys, panel passwords, OAuth credentials or reverse-proxy secrets that were ever visible outside the private deployment. The source archive does not contain them, but the running server still needs its own secret-rotation review.
4. Decide whether the license copyright line should name a person, organization or contributor group.
5. Review the upstream NOTICE and preserve it in forks and binary distributions.
6. Never push the private deployment's account files, logs, databases or server configuration.

## Repository settings after publishing

- Enable private vulnerability reporting and GitHub Security Advisories.
- Enable secret scanning and push protection when available.
- Enable Dependabot alerts and automated security updates.
- Require the CI test and container jobs before merging to main.
- Protect the main branch and release tags.
- Enable CodeQL code scanning.
- Add repository description and topics such as ai-gateway, openai-compatible, workbuddy and self-hosted.
- Create the final support contact and code-of-conduct reporting channel.
- Publish the first release only after the release safety workflow passes.

## Data boundary

A public source tree may contain code and synthetic test fixtures only. Do not publish a database dump, account export, request log, browser screenshot containing identifiers, stack trace containing tokens or environment file.
