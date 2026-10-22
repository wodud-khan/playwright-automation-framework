# Design Decisions

The small owned application makes UI, API, JSON, and SQL observations reproducible without depending on a public demo site. The full cross-layer flow runs on Chromium; a page smoke test covers Firefox and WebKit. Those are separate scopes.

The UI exposes customer, item, and quantity while fixing price at 2499 cents. Tests specify expected totals independently in cents. The page object handles interaction and display checks; test fixtures own record cleanup. API tests require exact product statuses, while teardown accepts a previously deleted owned ID only after it verifies 404 by exact ID.

Serial runs are the diagnostic default. Two-worker service and UI runs check isolation without unbounded workers. Playwright's semantic locators and observable waits are preferred for this page. Blanket reruns are absent because they can hide an initial failure; a targeted retry would need its own evidence and justification. The existing toolchain and report formats are kept small enough to explain.

See [architecture](ARCHITECTURE.md) for components and [flaky-test policy](FLAKY_TEST_POLICY.md) for triage.

## October 2026 review

The project is now **Playwright Automation Framework**, with the GitHub repository named
`playwright-automation-framework`. This describes the tool and purpose directly while
the README explains the broader API, contract, and database coverage. Python package
imports remain `demo_app` and `test_framework`; they do not depend on the distribution
name or checkout directory. GitHub redirects the previous repository URL.

The tracked application, fixtures, clients, tests, packaging, container setup, workflow,
and documentation were reviewed. Existing page objects, native pytest-playwright fixtures,
explicit timeouts, locked dependencies, independent assertions, and exact-ID cleanup are
appropriate for the project. A new runner, generic base-page hierarchy, BDD layer, or a
rewrite in TypeScript would add migration cost without addressing an observed need.

The concrete improvements are bundled contract resources, error-response contracts,
parameterized HTTP input boundaries, finite timeout validation, a readiness probe that
honors the configured app URL, readable UI validation errors, narrow-screen layout and
keyboard checks, verified deletion before releasing ownership, parallel UI coverage in CI,
and scheduled dependency-update proposals. The README now separates the service-free
unit quick start from the full environment and links dated evidence instead of narrating
previous editing passes.

### Research informing the decisions

Reviewed October 22, 2026; these are design references, not evidence that this repository
has all the capabilities of the referenced projects.

| Primary source | Application here |
|---|---|
| [Microsoft's pytest plugin](https://github.com/microsoft/playwright-pytest) and [fixture reference](https://playwright.dev/python/docs/test-runners) | Keep native context/page fixtures and artifact options rather than managing browsers ourselves. |
| [Playwright locators](https://playwright.dev/python/docs/locators) | Keep role/label locators, with test IDs for displayed order values. |
| [Pydantic edge-case tests](https://github.com/pydantic/pydantic/blob/main/tests/test_edge_cases.py) | Use direct, parameterized boundary cases; avoid a custom test-case DSL. |
| [uv's GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/) | Retain locked sync and the official setup action. |
| [Dependabot ecosystem support](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories) | Propose updates to uv, Actions, and Docker through reviewable PRs. |
| [Playwright coding agents](https://playwright.dev/python/docs/getting-started-cli), [MCP](https://github.com/microsoft/playwright-mcp), and [test agents](https://playwright.dev/docs/test-agents) | Keep AI exploration optional; retain deterministic Python tests as the committed regression suite. |

The locked toolchain passes validation; there is no benefit in upgrading every package
solely to make version numbers look recent. Review dependency updates individually and run
the complete workflow. The Python 3.12 constraint remains until another interpreter line
is actually exercised. Performance testing, authentication, and broad accessibility auditing
need explicit product requirements and representative scenarios before expanding scope.

## Final security review

Python 3.12.15, pytest 9.1.1, certifi 2026.10.19, and urllib3 2.8.0 replace affected
versions identified during the final audit. The optional `security` dependency group
keeps Bandit and pip-audit out of the normal test installation. CI also scans complete Git
history and both container images using checksum-pinned scanner binaries.

Container scans justified replacing the older Debian bases with minimal Alpine 3.24
images. PostgreSQL stays on major version 17, upgraded to maintenance release 17.11.
The database target updates OS packages and removes gosu because it starts directly as
`postgres`; the application image removes unused pip. A separate named volume avoids
silently reusing data across libc/locale changes. The full clean-install suite validates
the new runtime, and previous local volumes remain untouched.

No extra AI runtime or alternative test runner was added. The existing optional
exploration workflow remains appropriate; model-generated changes still require the
same deterministic regression and security gates.
