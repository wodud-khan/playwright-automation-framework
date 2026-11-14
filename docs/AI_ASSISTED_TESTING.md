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

## From requirements to validation

This branch records a real Codex-assisted design and implementation exercise. Start
with [AGENTS.md](../AGENTS.md), the [approved demonstration requirements](ai-qa/order-requirements.md),
[decision table](ai-qa/decision-table.md), and [traceability](ai-qa/traceability.md).
The owner approved the baseline and three test groups; personal review of the final
code remains pending. [AI review](ai-qa/ai-review-log.md) and
[execution evidence](ai-qa/validation.md) record different kinds of verification.

| Step | Input and action | Reviewable output |
|---|---|---|
| Requirements → AI analysis | Give Codex the supplied specification, source paths, scope, and [requirements prompt](../prompts/requirements-analysis.md). Reconstruct only what source supports. | Stable IDs, acceptance criteria, observations, assumptions, and owner questions |
| Test scenarios | Derive positive/negative cases, boundaries, partitions, and meaningful decisions. | Scenario/decision table; owner approval of material reconstructed expectations |
| Coverage review | Use the [coverage prompt](../prompts/coverage-analysis.md) to compare actual assertions with the specification. | Prioritized add/defer choices with existing function references and risk |
| Python generation | Use the [generation prompt](../prompts/test-generation.md) for approved scenarios. Reuse existing fixtures and cleanup. | Small Python diff with independent expected values and requirement mapping |
| Human review | Use the [review prompt](../prompts/test-review.md) as a checklist; the owner inspects the generated diff and AI findings. | Recorded acceptance or requested changes; no inferred approval |
| Test execution | Run README setup and existing pytest/static checks against the required environment. Execution can inform review before final acceptance. | Exact commands, output, reports, and environment details |
| Failure investigation | Use the [debugging prompt](../prompts/debug-and-retest.md) with original failure evidence. | Reproduced case and evidence-backed product/test/environment/cleanup classification |
| Correction → retesting | Make the smallest justified change; obtain owner review if expectations change. Retest the original case and affected suite. | Preserved first failure plus subsequent result; no assertion weakening |
| Validation report | Consolidate commands, outcomes, limitations, and remaining review decisions. | Dated evidence tied to the actual working tree or commit |

For example, this exercise selected numeric API corners, omitted required fields,
and name-length unit boundaries. Review of the first draft found unsafe duplication
of creation/ownership handling; the implementation now supplies boundary data to the
existing manager. The log records that actual correction rather than inventing a
historical AI incident. Ordinary regression coverage remains model-independent:
neither pytest nor CI calls Codex, Claude Code, or a model provider.

The prompts can also be supplied to Claude Code or another coding assistant that can
read the repository. That portability is a proposed workflow, not evidence of a
Claude Code execution here. Model-generated findings still need source inspection,
deterministic execution, and personal owner review. Future evaluation/agent/RAG work
is described only in the [roadmap](AI_QUALITY_ENGINEERING_ROADMAP.md).

This documents an optional workflow, not a claim of validated autonomous or self-healing
coverage. No model-dependent step runs in CI.
