# Optional AI-assisted testing

AI can help explore the demo, suggest boundary cases, draft tests, and inspect failure
traces. It is a development aid; the committed pytest suite runs without a model, API key,
Node.js, or MCP server.

Playwright's [coding-agent guide](https://playwright.dev/python/docs/getting-started-cli)
describes its CLI for coding agents and MCP for persistent browser exploration. Both are
optional tools with their own installation requirements. Follow that guide if you already
use a compatible agent. The [test-agent workflow](https://playwright.dev/docs/test-agents)
uses Playwright Test artifacts such as TypeScript specs; it is not a drop-in pytest runner.
No untested MCP configuration or second JavaScript test stack is bundled here.

## A useful exploration task

Start the local stack from the README, then give your browser-capable agent this brief:

> Explore only the local Order Lab at http://127.0.0.1:8000. Review required fields,
> quantity boundaries, keyboard navigation, and validation feedback. Record observed
> behavior separately from assumptions. Use synthetic data, record every created order ID,
> and delete only those IDs through the API. Suggest focused pytest tests using the existing
> OrderPage, OrderFactory, and OrderManager. Do not change expected results to make failures
> pass or add retries, sleeps, or new dependencies.

Review each suggestion against the application requirements. Put pure validation logic
in unit tests, HTTP behavior in API tests, and only browser behavior in UI tests. Use the
existing manager for records created by a test and register UI-created IDs before assertions.

Run the affected tests and the normal quality checks before accepting a generated change.
For a reported defect, first reproduce the failure and then verify that the correction
passes the same case. Preserve the original failure evidence; automatic locator “healing”
must not silently change the behavior being tested. Inspect traces and console text before
sending them to any external model service.

This documents an optional workflow, not a claim of validated autonomous or self-healing
coverage. No model-dependent step runs in CI.
