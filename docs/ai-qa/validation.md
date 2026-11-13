# AI-assisted QA validation — 2026-11-13

Scope: local working tree on `feat/ai-assisted-qa-evidence`, based on
`92df19f146908a0e38ad9d633f4c596137463d25`. This report validates the current changes,
not a new hosted CI run. Earlier [validation](../VALIDATION.md) and the
[historical report](../FINAL_VALIDATION_REPORT.md) remain unchanged.

## Environment and setup

macOS ARM64; Python 3.12.15; pytest 9.1.1; Playwright 1.61.0; Pydantic 2.13.4;
Docker Engine 29.6.2; Compose v5.3.1; PostgreSQL 17.11. Browser binaries were already
cached, and the install command completed successfully. Service/browser tests used
the existing Compose stack with actual PostgreSQL; no SQLite UI fallback was used.
SQLite tests remain isolated unit evidence.

Initial uv was 0.11.8. A supported PyPI installation placed uv 0.13.5 in a temporary
tools directory without modifying dependencies or the global executable:

```bash
UV_CACHE_DIR=/private/tmp/ai-qa-uv-cache uv pip install \
  --python .venv/bin/python --target /private/tmp/ai-qa-tools 'uv==0.13.5'
export PATH="/private/tmp/ai-qa-tools/bin:$PATH"
uv --version
uv sync --extra dev --locked --python 3.12.15
docker desktop start
docker compose up --detach --build --wait
uv run --frozen playwright install chromium firefox webkit
export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
export TEST_RUN_ID=ai-qa-20261113
uv run --frozen python scripts/wait_for_services.py --timeout 30
```

All setup commands above ultimately exited 0. The temporary uv path is specific to
this run; normal users should follow README installation. The first uv installation
attempt failed because sandbox DNS access was restricted; the same command succeeded
with network access. Initial Docker inspection was sandbox-restricted, and subsequent
inspection showed the daemon stopped. Starting Docker Desktop resolved that limitation.
No Docker data reset or volume deletion was performed.

The initial dev-only sync removed optional security tools from the local environment;
the later locked security-group sync below restored them. `pyproject.toml` and
`uv.lock` were not changed.

## Static and unit results

| Exact command | Actual result |
|---|---|
| `uv lock --check` | Passed; resolved 75 packages |
| `uv run --frozen ruff check .` | Passed |
| `uv run --frozen ruff format --check .` | Initially failed for one new API-test call; passed after formatting |
| `uv run --frozen ruff format tests/api/test_orders_api.py` | Corrected formatting in one file; no behavior change |
| `uv run --frozen mypy src scripts` | Passed; 18 source files |
| `uv run --frozen pytest --collect-only -q` | Passed; 104 collected with default Chromium configuration |
| `uv run --frozen pytest tests/unit -q` | 72 passed |
| `uv run --frozen pytest tests/unit -q -n 2 --html=artifacts/ai-qa-20261113/unit-report.html --self-contained-html --junitxml=artifacts/ai-qa-20261113/unit-junit.xml` | 72 passed |

The first lint/format/Mypy chain stopped at the formatting failure; Mypy then ran
successfully in the subsequent check. No test assertion or application expectation
was weakened to obtain a passing result.

## Service and browser results

Reports below are retained locally under ignored `artifacts/ai-qa-20261113/`.
The serial runs executed all 104 collected cases across unit (72), service (23),
and Chromium UI/E2E (9) invocations. This is not a claim of one combined pytest run
or 100% behavioral coverage. Parallel and smoke runs are additional executions.

| Exact command | Actual result |
|---|---|
| `uv run --frozen pytest tests/api tests/contract tests/database tests/integration -q --html=artifacts/ai-qa-20261113/service-report.html --self-contained-html --junitxml=artifacts/ai-qa-20261113/service-junit.xml` | 23 passed against PostgreSQL |
| `uv run --frozen pytest -m 'api or contract or database or integration' -q -n 2 --junitxml=artifacts/ai-qa-20261113/service-parallel-junit.xml` | 23 passed; `TEST_RUN_ID=ai-qa-20261113-parallel` |
| `uv run --frozen pytest tests/ui tests/e2e -q --browser chromium --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure --output artifacts/ai-qa-20261113/playwright/chromium --html=artifacts/ai-qa-20261113/browser-report.html --self-contained-html --junitxml=artifacts/ai-qa-20261113/browser-junit.xml` | 9 passed |
| `uv run --frozen pytest -m smoke -q --browser chromium --browser firefox --browser webkit --tracing retain-on-failure --screenshot only-on-failure --output artifacts/ai-qa-20261113/playwright/smoke --junitxml=artifacts/ai-qa-20261113/browser-smoke-junit.xml` | 3 passed, 115 deselected; `TEST_RUN_ID=ai-qa-20261113-smoke` |
| `uv run --frozen pytest tests/ui -q -n 2 --browser chromium --tracing retain-on-failure --screenshot only-on-failure --output artifacts/ai-qa-20261113/playwright/parallel --junitxml=artifacts/ai-qa-20261113/browser-parallel-junit.xml` | 6 passed; `TEST_RUN_ID=ai-qa-20261113-browser-parallel` |

The passing browser suite includes existing controlled child-test failures for cleanup
and diagnostics. Those expected failures are checked by passing outer regressions;
they are not new AI-generated incidents or ignored product failures.

Additional executed container checks:

```bash
docker compose exec -T -w /tmp app python -c \
  'from test_framework.contracts import load_schema; from jsonschema import Draft202012Validator; [Draft202012Validator.check_schema(load_schema(name)) for name in ("order.schema.json", "error.schema.json")]'
docker compose exec -T database psql -U portfolio -d portfolio -Atc 'SHOW server_version'
```

Both passed. Installed package schemas validated outside the source working directory;
the server reported 17.11. This does not replace runtime response contract tests.

## Security checks and CI limits

```bash
uv sync --extra dev --group security --locked --python 3.12.15
uv run --frozen bandit -r src scripts conftest.py
uv export --locked --extra dev --group security --no-emit-project \
  --format requirements-txt --output-file /private/tmp/ai-qa-requirements-audit.txt > /dev/null
uv run --frozen pip-audit -r /private/tmp/ai-qa-requirements-audit.txt --no-deps --disable-pip
```

All exited 0. Bandit scanned 984 lines with no issues or suppressions. pip-audit
reported no known vulnerabilities at execution time; it emitted advisory warnings
about `--no-deps` and hashes under the existing CI command. This is not a security
certification or a guarantee against future advisories.

Gitleaks history and Trivy image scans were **not run during the initial validation**;
neither executable was then available. The follow-up below records their later execution.
Their CI definitions remain unchanged. Hosted GitHub Actions: **not run for this branch**,
because it has not been pushed and no PR has been opened. Local checks do not establish
a hosted CI pass. No external model was needed by any regression.

## Cleanup and review

```bash
mkdir -p artifacts/ai-qa-20261113
docker compose ps --all > artifacts/ai-qa-20261113/compose-ps.txt
docker compose logs --no-color > artifacts/ai-qa-20261113/compose.log
docker compose exec -T database psql -U portfolio -d portfolio -Atc 'SELECT count(*) FROM orders'
docker compose down
git diff --check
```

The count was 0 after all test runs. Compose diagnostics were saved, stack shutdown
succeeded, and the named database volume was retained. `git diff --check` passed.
No table-wide deletion was performed. Reports and raw diagnostic artifacts remain
untracked and should be inspected before sharing.

A one-off Python inspection checked all 18 changed/new files, 80 local Markdown
links, and documented test-function references without finding missing targets or
trailing whitespace. Parsing the six JUnit reports confirmed the case counts above
and zero failure/error elements. No permanent checker or additional dependency was added.

Codex's [entire-diff review](ai-review-log.md) found and corrected draft ownership
handling, strengthened field-specific unit assertions, applied required formatting,
and corrected a documentation typo. Personal owner review of the final code remains
pending. Numeric coercion policy, deferred normalization/padded-length cases, and
absent hosted CI evidence remain explicit limitations.

This is personal-project evidence for specification-driven design, AI-output review,
and independently executed Python QA automation. It does not establish prior employment,
a live AI evaluation system, or an implemented agent/RAG capability.

## Autonomous completion follow-up — 2026-11-13

The owner authorized autonomous completion and local commits on the existing feature
branch, while retaining the prohibition on pushes, PR creation, merging, and changes
to `main`. No additional product requirement or future roadmap module was implemented.

### Remaining scanners and actual image correction

Installed the CI-pinned Gitleaks 8.30.1 and Trivy 0.76.1 macOS ARM64 binaries in
`/private/tmp/ai-qa-scanners`. Archives came from each project's official GitHub release;
Python SHA-256 comparisons against the release checksum manifests succeeded:

| Archive | Verified SHA-256 |
|---|---|
| `gitleaks_8.30.1_darwin_arm64.tar.gz` | `b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5` |
| `trivy_0.76.1_macOS-ARM64.tar.gz` | `11a9b6cd2752011b54f01ea4bd0dbfa9f0c41dc6538d5a3f9d23955f471bf4e5` |

Executed commands:

```bash
/private/tmp/ai-qa-scanners/gitleaks git . --log-opts='--all --full-history' \
  --redact=100 --report-format json \
  --report-path artifacts/ai-qa-20261113/gitleaks-history.json
/private/tmp/ai-qa-scanners/gitleaks dir /private/tmp/ai-qa-scanners/source-snapshot \
  --redact=100 --report-format json \
  --report-path artifacts/ai-qa-20261113/gitleaks-source.json
```

Both passed with zero findings. History scanning covered 29 pre-feature commits.
A one-off Python copy constructed the source snapshot from `git ls-files` plus
non-ignored new files; private configuration and generated artifacts were excluded.
Final staged-diff scanning is recorded in the completion report.

The previous image tags were no longer available during follow-up inspection.
`docker compose up --detach --build --wait` rebuilt and started the controlled stack
successfully. One automatic approval review timed out; its permitted retry completed.
No volume reset or unrelated Docker cleanup was performed.

```bash
/private/tmp/ai-qa-scanners/trivy image --cache-dir /private/tmp/ai-qa-scanners/trivy-cache \
  --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --timeout 5m --format json \
  --output artifacts/ai-qa-20261113/trivy-app.json playwright-automation-framework-app:latest
/private/tmp/ai-qa-scanners/trivy image --cache-dir /private/tmp/ai-qa-scanners/trivy-cache \
  --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --timeout 5m --format json \
  --output artifacts/ai-qa-20261113/trivy-database.json playwright-automation-framework-database:latest
```

The first app scan exited 1: 16 HIGH findings in inherited `krb5-libs` 1.22.2-r1,
with fixed version 1.22.3-r0 identified by the scanner. The database image scan exited
0 with no HIGH/CRITICAL findings. These are image inventory findings, not evidence
that an application exploit was reproduced.

The app-stage `Dockerfile` now runs `apk upgrade --no-cache` before the existing pip
removal, following the existing database-stage convention. This patches inherited OS
packages without changing application rules, Python dependencies, or the lockfile.
After another successful `docker compose up --detach --build --wait`:

```bash
/private/tmp/ai-qa-scanners/trivy image --cache-dir /private/tmp/ai-qa-scanners/trivy-cache \
  --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --timeout 5m --format json \
  --output artifacts/ai-qa-20261113/trivy-app-patched.json playwright-automation-framework-app:latest
```

The same gate exited 0 with zero HIGH/CRITICAL findings. The original failed scan is
preserved alongside the corrected report. No ignore rule, severity relaxation, or
scanner-version change was used. These local ARM64 scans do not establish hosted
Linux/x64 results or the absence of findings below the selected severity threshold.

### Full-suite retesting and final review

A follow-up static command initially failed because uv's default cache was outside
the writable sandbox. Setting `UV_CACHE_DIR=/private/tmp/ai-qa-uv-cache` resolved it;
Ruff lint, formatting, and Mypy then passed again without a code change.

The complete suite passed once before the OS patch (104 passed in 12.48s), then again
afterward (104 passed in 9.78s). Earlier reports remain intact. Both runs used the same
local URLs above and `UV_CACHE_DIR=/private/tmp/ai-qa-uv-cache`. Exact commands:

```bash
export PATH="/private/tmp/ai-qa-tools/bin:$PATH"
export UV_CACHE_DIR=/private/tmp/ai-qa-uv-cache
export TEST_RUN_ID=ai-qa-20261113-final
uv run --frozen python scripts/wait_for_services.py --timeout 30
uv run --frozen pytest -q --browser chromium --tracing retain-on-failure \
  --screenshot only-on-failure --video retain-on-failure \
  --output artifacts/ai-qa-20261113-final/playwright \
  --html=artifacts/ai-qa-20261113-final/full-report.html --self-contained-html \
  --junitxml=artifacts/ai-qa-20261113-final/full-junit.xml
export TEST_RUN_ID=ai-qa-20261113-patched
uv run --frozen python scripts/wait_for_services.py --timeout 30
uv run --frozen pytest -q --browser chromium --tracing retain-on-failure \
  --screenshot only-on-failure --video retain-on-failure \
  --output artifacts/ai-qa-20261113-final/patched/playwright \
  --html=artifacts/ai-qa-20261113-final/patched/full-report.html --self-contained-html \
  --junitxml=artifacts/ai-qa-20261113-final/patched/full-junit.xml
```

The final entire-diff review includes the Dockerfile correction and
[completion report](completion-report.md). No outstanding implementation defect was
identified within the approved scope. Personal owner code review has not occurred;
it is distinguished from the completed Codex review and is not a blocker to the
authorized local completion. Hosted CI remains unexecuted.

Final installed-package schema verification passed again. The post-patch Trivy report
lists `krb5-libs` 1.22.3-r0 in app image
`sha256:46f5ae8251eb555bd5467c92767e54ad87b03ad2a5082e1569ee120a4e84e32f`.
The scanned database image was
`sha256:956d8b1745f0b70944feacc556234e37ff658454b3dfc8f5a5b5c03a70765b0f`;
the subsequent build reused its filesystem layers. The final read-only SQL count
was 0. Post-patch Compose state/logs are under
`artifacts/ai-qa-20261113-final/patched/`; `docker compose down` succeeded again with
the named volume retained.

The final one-off document inspection checked all 20 changed/new files and 106 local
Markdown links, plus documented test-function references, without finding missing
targets or trailing whitespace. Parsing the post-patch JUnit report confirmed 104
cases, zero failures, and zero errors. Staged whitespace and secret checks passed:

```bash
git diff --cached --check
git diff --cached --no-ext-diff --unified=0 | /private/tmp/ai-qa-scanners/gitleaks stdin \
  --redact=100 --report-format json \
  --report-path artifacts/ai-qa-20261113/gitleaks-staged.json
```
