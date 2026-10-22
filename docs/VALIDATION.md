# Validation — October 22, 2026

Validated locally on macOS ARM64 with Python 3.12, uv 0.11.8, the committed lockfile,
and the PostgreSQL Compose stack. These results cover the October modernization changes;
older evidence remains in [the historical report](FINAL_VALIDATION_REPORT.md).

| Gate | Result |
|---|---|
| Locked development sync and `uv lock --check` | Passed; dependency versions unchanged |
| Ruff lint and format check | Passed |
| Mypy, `src scripts` | Passed, 18 source files |
| Full suite, PostgreSQL and Chromium | 85 passed |
| Unit suite, two workers | 61 passed |
| API/contract/database/integration, two workers | 15 passed |
| Focused Chromium UI, two workers | 6 passed |
| Chromium/Firefox/WebKit smoke | 3 passed |
| Non-editable package contract loading from `/tmp` in container | Both schemas loaded and validated |
| Compose build and readiness | Passed |

The full suite includes three E2E cases, including a child pytest process that deliberately
fails after creating an order. The outer regression verifies its exact-ID cleanup and
native trace, screenshot, video, and custom evidence. This expected child failure is part
of the passing suite, not an ignored product failure.

An initial service run overlapped the schema relocation and encountered two missing-file
failures. That interrupted run is not counted as baseline validation. The complete final
suite passed after the file changes and container rebuild were finished.

A final database inspection found only two pre-existing demo rows dated July 27. Those
rows were preserved; no records from this validation remained. The project stack was
stopped without deleting its named volume. Local JUnit reports are under the ignored
`artifacts/october/` directory.

Hosted results are available in [GitHub Actions](https://github.com/wodud-khan/sdet-playwright-framework/actions/workflows/quality.yml).
Check the run's commit before using it as evidence. Local success does not by itself
establish hosted success, zero flakiness, or coverage beyond the documented test scopes.
