# SDET Playwright Framework

[![Quality validation](https://github.com/wodud-khan/sdet-playwright-framework/actions/workflows/quality.yml/badge.svg)](https://github.com/wodud-khan/sdet-playwright-framework/actions/workflows/quality.yml)

A Python test automation portfolio covering an order workflow from browser to API to
PostgreSQL. A small FastAPI application is included so every layer runs against a
controlled system, without depending on public demo sites.

**Stack:** Python 3.12 · pytest · Playwright · Requests · JSON Schema · psycopg ·
PostgreSQL · Docker Compose · uv · Ruff · Mypy · GitHub Actions

## Start here

For a short code review, follow the [E2E workflow](tests/e2e/test_order_workflow.py),
[page object](src/test_framework/pages/order_page.py), and
[order cleanup manager](src/test_framework/order_manager.py). The
[failure drill](tests/e2e/test_failure_cleanup.py) proves that a failed browser assertion
still cleans up its order and produces diagnostic artifacts.

| Layer | What it demonstrates |
|---|---|
| Unit | Input rules, repository behavior, configuration, cleanup, diagnostics, readiness |
| API | Create/read/delete behavior and invalid input boundaries |
| Contract | Independent JSON schemas for successful and error responses |
| Database | Exact persisted values read directly with psycopg |
| Integration | API deletion verified through API and PostgreSQL |
| UI | Required fields, error feedback, keyboard navigation, mobile layout |
| E2E | UI creation, contract checks, API/SQL verification, and targeted cleanup |

The full workflow runs on Chromium. A page smoke test runs on Chromium, Firefox, and
WebKit. Focused keyboard and layout checks are not a complete accessibility audit.

## Run locally

Install [uv](https://docs.astral.sh/uv/) first. The unit suite needs neither Docker nor
browser binaries:

```bash
git clone https://github.com/wodud-khan/sdet-playwright-framework.git
cd sdet-playwright-framework
uv sync --extra dev --locked --python 3.12
uv run --frozen pytest tests/unit -q
```

For all layers, start Docker with Compose support and run:

```bash
uv run --frozen playwright install chromium firefox webkit
docker compose up --detach --build --wait
export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
uv run --frozen python scripts/wait_for_services.py --timeout 30
uv run --frozen pytest -q --browser chromium
```

On Linux, use `playwright install --with-deps chromium firefox webkit` to install browser
system dependencies as well. View the demo at `http://127.0.0.1:8000` and its OpenAPI
explorer at `/docs`.

For narrower or parallel runs:

```bash
uv run --frozen pytest tests/api tests/contract tests/database tests/integration -q
uv run --frozen pytest -m 'api or contract or database or integration' -q -n 2
uv run --frozen pytest tests/ui -q -n 2 --browser chromium
uv run --frozen pytest -m smoke -q --browser chromium --browser firefox --browser webkit
```

Stop the stack with `docker compose down`; the named database volume is retained.
If ports 8000 or 5432 are occupied, set Compose's `APP_PORT`/`POSTGRES_PORT` and the
matching `APP_BASE_URL`/`DATABASE_URL`. The readiness script follows `APP_BASE_URL`.
See [troubleshooting](docs/TROUBLESHOOTING.md) for examples and the optional SQLite UI
path. SQLite checks do not substitute for PostgreSQL integration tests.

## Engineering choices

- Function-scoped browser contexts and uniquely generated records keep tests isolated.
- Cleanup addresses only registered order IDs, attempts every ID, and verifies absence.
- Semantic locators, Playwright assertions, and response events replace fixed sleeps.
- Standalone [JSON schemas](src/test_framework/schemas) stay independent of application
  models and are bundled in installed packages.
- Tests specify expected totals independently of the application's calculation.
- No blanket retries: unexpected browser errors and failed cleanup remain visible failures.
- Locked dependencies and SHA-pinned CI actions provide a repeatable baseline. Dependabot
  proposes monthly updates for review; updates are not automatically merged.

## Quality checks and debugging

```bash
uv lock --check
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy src scripts
uv run --frozen pytest tests/ui tests/e2e --browser chromium \
  --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure \
  --output artifacts/playwright --junitxml=artifacts/browser-junit.xml \
  --html=artifacts/browser-report.html --self-contained-html
```

Mypy checks application/framework code and scripts. CI also runs unit and service tests,
Chromium UI/E2E, bounded parallel checks, and three-engine smoke. It uploads reports and
stops its Compose stack. It does not deploy the application.

Custom failure JSON includes API exchange metadata and browser error events. Native traces,
screenshots, videos, and raw console text can contain sensitive data; use synthetic inputs
and review artifacts before sharing. Teardown-only failures may lack native failure
artifacts; use `--tracing on` for that reproduction. See the
[diagnostic guide](docs/TROUBLESHOOTING.md) for cleanup and evidence limitations.

## Further reading

- [Architecture](docs/ARCHITECTURE.md) and [test strategy](docs/TEST_STRATEGY.md)
- [Design decisions and modernization review](docs/DESIGN_DECISIONS.md)
- [Optional AI-assisted testing](docs/AI_ASSISTED_TESTING.md)
- [CI guide](docs/CI_CD_GUIDE.md) and [flaky-test policy](docs/FLAKY_TEST_POLICY.md)
- [Current validation](docs/VALIDATION.md) and [historical evidence](docs/FINAL_VALIDATION_REPORT.md)

This is a focused, team-adaptable framework, not a production application. Authentication,
schema migrations, load testing, and comprehensive security/accessibility testing are
outside its demonstrated scope.
