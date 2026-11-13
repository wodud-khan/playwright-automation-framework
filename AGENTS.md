# Repository instructions

## Architecture and scope

This is a Python 3.12 portfolio: pytest, pytest-playwright, Requests, JSON Schema,
psycopg, FastAPI, PostgreSQL, uv, Ruff, Mypy, and GitHub Actions. Keep that stack.
`src/demo_app` is the controlled system under test; `src/test_framework` contains
clients, data, cleanup, diagnostics, and page objects. Do not rewrite working code,
add another runner, or implement future roadmap stages without an explicit task.

## Requirements and test placement

- Read the supplied specification and [approved order baseline](docs/ai-qa/order-requirements.md).
  Identify requirement IDs and acceptance criteria before proposing assertions.
  Separate approved expectations, observed implementation, and assumptions. Ask the
  owner about material ambiguities; leave unresolved policies out of authoritative tests.
- Put isolated validation/helper tests in `tests/unit`, HTTP behavior in `tests/api`,
  independent response-schema checks in `tests/contract`, direct psycopg checks in
  `tests/database`, API/SQL lifecycle checks in `tests/integration`, focused browser
  behavior in `tests/ui`, and complete UI/API/SQL workflows in `tests/e2e`.
- Use the matching registered pytest marker. Prefer small parameterized tests over
  repeated bodies. Cover risk and distinct behavior; do not repeat every case at every layer.
- Keep expected totals independent: use reviewed literal cases or independently
  specified arithmetic. Do not import application calculation logic as the test oracle.
  Contract checks use the standalone schemas in `src/test_framework/schemas`.

## Fixtures, data, and cleanup

Use `conftest.py` fixtures: `api_client`, `postgres_client`, `order_factory`,
`order_manager`, `service_settings`, `ui_settings`, and the native `page` fixture.
`OrderManager.create()` builds a unique order; an explicit `OrderData` payload may
be supplied for approved variations. Use `dataclasses.replace` on factory data.
Keep creation through the manager when possible so unexpected-status ownership
verification and teardown remain in one place.

For UI creation, register the returned exact ID with `order_manager.register_owned`
before result assertions. Call `mark_cleaned` only after explicitly verifying deletion
through API and PostgreSQL. Fixture teardown deletes remaining registered IDs and
checks API absence; it attempts every ID and surfaces cleanup failures.

Use synthetic data only. Preserve factory run/worker/random suffixes for service
records. Short fixed boundary strings belong in isolated unit tests. Never use real
customer data, delete unowned records, truncate tables, reset volumes, or suppress
cleanup errors. Run mutations only against the controlled local Compose application,
not public or production systems. Preserve named volumes with `docker compose down`.

## Browser conventions and diagnostics

Extend `OrderPage` instead of duplicating interactions. Prefer `get_by_role` and
`get_by_label`; existing test IDs identify displayed order values. Use Playwright
`expect`, response events, and auto-waiting. Avoid sleeps, brittle DOM selectors,
blanket retries, and silent locator healing. Preserve function-scoped contexts.

The autouse `browser_evidence` fixture fails on unexpected browser errors. Register
only deliberately expected HTTP errors by exact method/path/status/count before
triggering them. Preserve the first failure and API/browser evidence. Classify
product, test, environment, and cleanup failures before correcting code. Never
silently weaken, remove, or alter an assertion merely to obtain a passing result.
Document the reason and requirement for an expectation change; obtain owner review
when it changes the accepted behavior. Retest the original failing case, then the
affected suite. Review raw traces, screenshots, video, and console text before sharing.

## Validation and Definition of Done

Follow README setup: uv >=0.13.5, Python 3.12.15, locked dev dependencies. Run:

```bash
uv lock --check
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy src scripts
uv run --frozen pytest tests/unit -q
```

For service changes, start the documented Compose stack, export its matching local
URLs, run readiness, then serial service tests and relevant Chromium UI/E2E tests.
Run the existing two-worker checks and three-browser smoke when validating isolation
or browser scope. SQLite unit/UI fallback results are not PostgreSQL evidence.
CI additionally collects tests, runs unit tests on two workers, checks installed
contracts, and runs Gitleaks, Bandit, pip-audit, and Trivy. See `quality.yml` for exact
commands; do not describe configured CI as an executed hosted run.

Done means the diff is reviewed for correctness, maintainability, duplication, weak
assertions, cleanup, and misleading claims; affected tests and required checks have
actual results; traceability and dated validation reflect those results; limitations
and pending owner decisions are explicit. Keep AI proposals separate from execution
evidence and distinguish AI review from personal owner review. Regression execution
requires no model key or agent runtime. Preserve historical validation records.
Do not push or merge without explicit permission.
