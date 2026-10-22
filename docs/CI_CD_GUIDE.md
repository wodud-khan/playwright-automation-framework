# CI Guide

`.github/workflows/quality.yml` has three jobs. The `security` job scans complete Git history with a checksum-pinned Gitleaks binary, runs Bandit, and audits the locked runtime, development, and security dependencies with pip-audit. `static-and-unit` installs the locked Python 3.12 environment, checks the lock, collects tests, runs Ruff and Mypy, and runs unit tests with two workers. `postgres-and-browser` waits for both prerequisite jobs, then builds the Compose stack, waits for health, runs serial and two-worker service suites, Chromium UI/E2E, and Chromium/Firefox/WebKit smoke. It captures Compose logs, stops the stack without deleting the volume, and uploads reports under `if: always()`.

The workflow has read-only repository permissions, non-persisted checkout credentials, job timeouts, concurrency cancellation, and SHA-pinned actions. It runs on pull requests, pushes to `main`, and manual dispatch. It validates quality; it does not deploy, publish, or release. Local commands and port overrides are in the [README](../README.md). Historical run links are in the [validation record](FINAL_VALIDATION_REPORT.md).

The workflow also runs focused Chromium UI tests with two workers. Monthly Dependabot
proposals cover uv, SHA-pinned Actions, Dockerfile images. Review the
resolved versions and CI results before merging; there is no automatic merge policy.
When updating uv, keep the workflow's `UV_VERSION` and Dockerfile stage aligned.

Artifact uploads use explicit report, diagnostic, and browser paths instead of the entire
artifact directory. Security reports are not uploaded. CI uses only synthetic demo data.

Python feature-version and PostgreSQL major-version Docker updates require an explicit
compatibility review. Dependabot continues to propose patch updates within those lines.

After building the stack, a checksum-pinned Trivy binary scans both images and blocks
high/critical vulnerabilities, including unfixed advisories. Builds use official Alpine
bases, a patched PostgreSQL 17 maintenance release, and non-root runtime users. The
`database` target applies available Alpine package updates at build time.
