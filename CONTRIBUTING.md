# Contributing

Thanks for helping improve WorkBuddy2API Hub.

## Before opening an issue

- Search existing issues first.
- Use a minimal reproduction with secrets removed.
- Never attach <code>accounts/</code>, <code>usage/</code>, <code>logs/</code>, <code>.env</code> files, token exports or database files.
- Report security problems privately as described in [SECURITY.md](SECURITY.md).

## Development setup

Requirements:

- Python 3.11 or newer
- Docker, optional for container testing
- No third-party Python runtime dependency is required

Create an isolated test environment:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
~~~

Do not point tests at a real account directory. Use temporary directories and the <code>--accounts-dir</code> / <code>--usage-dir</code> options.

## Pull requests

- Keep each pull request focused.
- Explain the user-facing behavior and security impact.
- Add or update tests for behavior changes.
- Update documentation and [CHANGELOG.md](CHANGELOG.md) when appropriate.
- Confirm that CI passes.
- Do not include generated data, runtime logs, screenshots containing identifiers or unrelated formatting churn.

## Style

- Python 3.11 compatible
- Four spaces in Python
- Prefer the standard library unless a dependency has a clear operational benefit
- Preserve public API compatibility unless the pull request explicitly documents a breaking change
- Use descriptive variable names and comments that explain why, not what

## Commit messages

Use short imperative subjects, for example:

~~~text
fix: reject downloads from unauthorized sessions
docs: document safe LAN deployment
test: isolate account directory in smoke test
~~~

## License

By submitting a contribution, you agree that it may be distributed under this repository's MIT license.
