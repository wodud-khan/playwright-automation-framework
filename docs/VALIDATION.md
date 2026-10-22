# Final validation — October 22, 2026

Validated on macOS ARM64 using a fresh source directory and virtual environment,
Python 3.12.15, uv 0.13.5, pytest 9.1.1, and the committed lockfile. The final stack
uses Python 3.12.15 and PostgreSQL 17.11 on Alpine 3.24, with both services running
as non-root users and host ports bound to localhost.

| Executed check | Result |
|---|---|
| Clean README installation and browser install command | Passed |
| Locked sync and lock consistency | Passed |
| Ruff lint and formatting | Passed |
| Mypy, `src scripts` | Passed, 18 source files |
| Full suite against final PostgreSQL stack, Chromium | 88 passed |
| Unit suite, two workers | 64 passed |
| API/contract/database/integration, two workers | 15 passed |
| Focused Chromium UI, two workers | 6 passed |
| Chromium/Firefox/WebKit smoke | 3 passed |
| Explicit SQLite UI fallback | 6 passed |
| Installed distribution and bundled contracts, outside source directory | Passed |
| Gitleaks history, public source snapshot, and staged diff | No secrets detected |
| Bandit, application/framework/scripts/root fixtures | No findings or suppressions |
| pip-audit, 72 locked third-party packages including dev/security tools | No known vulnerabilities |
| Trivy, final app and database images on ARM64 | No reported vulnerabilities at any severity |
| Ignore probes for 17 sensitive/generated paths | All excluded; `.env.example` remains tracked |
| Docker context allowlist probe | Passed |

The full suite includes a controlled child test that fails after order creation. Its
passing outer regression verifies exact-ID cleanup and native trace, screenshot, video,
and custom evidence. Expected child failures are not ignored product failures.

Container auditing identified vulnerabilities in the former Python dependencies and
Debian-based images. The final images remove unused pip and gosu executables and use
patched Alpine packages. No vulnerability ignore list was introduced. CI independently
scans its Linux images and fails on high or critical findings; local scans included every
severity. See [security notes](../SECURITY.md) for scope and advisory references.

The rename creates a separate `portfolio_database_alpine` volume. Previous volumes and
demo data remain intact. Final test cleanup leaves no orders in the new volume. No volume
reset or history rewrite was performed.

Docker Desktop stalled when the session resumed. Its processes were restarted without a
data reset; the final image scans and all service/browser suites were then rerun successfully.
An initial fallback UI attempt could not bind its server within the execution sandbox;
all six tests passed after the server was started with loopback access.

Detailed local reports are intentionally untracked. Older results are retained in the
[historical report](FINAL_VALIDATION_REPORT.md). Verify the commit associated with the
[GitHub Actions run](https://github.com/wodud-khan/playwright-automation-framework/actions/workflows/quality.yml)
before citing hosted results. These checks do not constitute a penetration test or a claim
of production application readiness.
