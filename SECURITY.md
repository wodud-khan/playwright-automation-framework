# Security and privacy

This repository is a local automation demo, not an authenticated service. Use synthetic
data. Compose publishes the app and PostgreSQL on `127.0.0.1` only. The included database
password is a public demo value; never reuse it for a shared or production system.

## Before publishing changes

```bash
uv sync --locked --extra dev --group security
uv run --frozen bandit -r src scripts conftest.py
uv export --locked --extra dev --group security --no-emit-project \
  --format requirements-txt --output-file /tmp/playwright-audit-requirements.txt
uv run --frozen pip-audit -r /tmp/playwright-audit-requirements.txt --no-deps --disable-pip
gitleaks git . --log-opts='--all --full-history' --redact=100
git diff --cached --check
```

Install Gitleaks from its [official releases](https://github.com/gitleaks/gitleaks/releases)
and verify the release checksum. CI pins its binary version and checksum, checks full
history, and runs the locked Python security tools. It fails on scanner findings rather
than automatically suppressing or fixing them. Updating the Gitleaks version also requires
updating the checksum in the workflow.

Keep `.env`, private keys, browser authentication state, local agent notes, databases,
and test artifacts untracked. `.gitignore` protects common paths, but does not remove
tracked files or rewrite history. Before committing, inspect `git diff --cached` and
scan newly staged files as well as history. The Docker context admits only explicit
application build inputs; local notes and reports do not enter the image.

## Reports and traces

Custom evidence removes credentials, query strings, and fragments from structured URL
fields. Paths, raw console text, exceptions, native traces, screenshots, videos, and
pytest reports can still contain personal data or secrets. Ignore rules are not redaction.
Inspect archive contents and visual evidence before sharing. Keep sensitive evidence
private and generate a new synthetic reproduction for public discussion.

CI uses only synthetic test data and uploads a defined set of reports and diagnostics,
not the entire artifact directory. Audit reports stay out of public artifacts. Do not
point this workflow at a production system or supply real customer data or credentials.

## If a secret is exposed

Revoke or rotate it first, remove it from current files, then assess Git history, forks,
Actions logs, artifacts, and caches. Coordinate any history rewrite with repository owners;
deleting a file or adding an ignore rule does not undo an exposure. Report privately and
never paste credential values into a public issue.

## Final audit scope — October 22, 2026

The review covered tracked source and configuration, staged/public file snapshots, all
fetched Git branches and tags, local reports and trace archive contents, sampled video
frames, screenshots, and local SQLite databases. Initial history inspection covered 29
commits and 197 unique blobs. Gitleaks found no secrets; supplementary inspection found
only example email domains and a generic path-search pattern in historical source.
No credential requiring rotation was identified.

Old ignored traces contain personal filesystem paths. They remain local and are not
included in the commit or uploaded. Five local SQLite files contained no order rows.
Scanners do not prove arbitrary binary media or free-form text free of confidential data.

Dependency advisories were addressed by updating certifi to 2026.10.19, urllib3 to 2.8.0,
and pytest to 9.1.1. The runtime is pinned to Python 3.12.15, with uv 0.13.5 in CI and Docker.
References: [certifi advisory](https://github.com/advisories/GHSA-6q48-6c7w-9gw2),
[pytest advisory](https://github.com/advisories/GHSA-6w46-j5rx-g56g), and urllib3's
[chunk buffering](https://github.com/advisories/GHSA-vxq7-64xx-v4gw),
[Deflate loop](https://github.com/advisories/GHSA-gh4c-6fx4-qh6g), and
[proxy TLS](https://github.com/advisories/GHSA-8988-9cw3-xx77) advisories.

See [validation](docs/VALIDATION.md) for executed checks and limitations. Advisory results
are point-in-time observations, not a guarantee against undisclosed vulnerabilities.

Both final container images were scanned with Trivy 0.76.1 on ARM64, with no reported
vulnerabilities at any severity. The app uses Python 3.12.15 on Alpine 3.24; the database
uses PostgreSQL 17.11 on Alpine 3.24 with current OS package updates. Unused pip and gosu
executables are removed. Both services start as non-root users. Previous Debian database
volumes are preserved; the new volume is intentionally separate because libc and locale
changes are not treated as an implicit database migration.

CI scans its built images and blocks high/critical findings without ignoring unfixed
advisories. The Trivy binary version and SHA-256 are pinned in the workflow. Rebuild
regularly to pick up Alpine security updates; dependency and image scans must be repeated
because advisory databases change. PostgreSQL's maintenance update follows the
[17.11 release notes](https://www.postgresql.org/docs/17/release-17-11.html).

GitHub secret scanning and push protection are enabled. Dependabot security alerts/fix
proposals and private vulnerability reporting are enabled as well. Use the repository's
[private security report form](https://github.com/wodud-khan/playwright-automation-framework/security/advisories/new)
for sensitive reports.
