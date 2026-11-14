# AI Quality Engineering roadmap

Status date: 2026-11-13. Keep one repository,
`wodud-khan/playwright-automation-framework`, and its Python/pytest/Playwright,
FastAPI/PostgreSQL, and GitHub Actions foundation. This is a personal portfolio;
future capabilities below are not employment history or completed achievements.

## Evidence and scope

| Status | Capabilities and evidence |
|---|---|
| Existing foundation | Layered software regression tests, independent contracts/totals, synthetic data, exact-ID cleanup, diagnostics, and configured CI. [Earlier validation](VALIDATION.md) is historical; [this branch's validation](ai-qa/validation.md) records actual current execution. |
| Current Stage 1 implementation | Codex-assisted specification analysis, owner-approved ORD-001–011 baseline, reusable prompts, selected Python tests, traceability, and actual AI review findings. Final personal owner review is pending. |
| Future, unimplemented | Model evaluation harness, live assistant, tool-call evaluation, RAG, AI-specific security scenarios, and evaluation CI/reporting. No provider integration or golden dataset is included in this branch. |

## Stage 1 — AI-assisted QA foundation

Objective: demonstrate senior QA judgment in specification-driven automation and
review of AI-generated Python. Reuse the existing application and fixtures. The
architecture is the existing pytest suite plus repository context and reviewable
documents, without another runner or agent orchestrator.

Artifacts are `AGENTS.md`, `prompts/`, `docs/ai-qa/`, and targeted extensions of current
tests/helpers. The workflow covers requirements-to-test generation, boundary/negative
design, risk prioritization, coverage mapping, debugging, human approval, and the
existing CI quality gates. Codex was used here; Claude Code can consume the same
context/templates, but no Claude Code run has been demonstrated.

Acceptance: approved expectations, independent assertions, safe cleanup, reviewed
diff, and exact static/unit/PostgreSQL/browser results with limitations. Normal tests
need no model or credentials; development-assistant usage may have separate account
costs. Resume claims must cite the implemented code and recorded execution, and
distinguish owner scenario approval from final code review.

## Stage 2 — AI Evaluation Lab (future)

- **Objective/career relevance:** demonstrate Python-based LLM evaluation and prompt
  regression reasoning with a small controlled order-support assistant.
- **Architecture:** an optional assistant entry point and simple provider boundary;
  a Python evaluator scores frozen responses offline. Keep expected behavior and
  rubric definitions separate from provider calls and the ordinary application.
- **Reuse/files:** existing API contracts and synthetic data; possible
  `src/ai_lab/assistant.py`, `src/ai_lab/evaluation.py`, `evals/datasets/`,
  `evals/prompts/`, and `tests/evaluation/`. These paths are proposals, not current files.
- **Testing:** human-reviewed golden cases with provenance and expected behavior;
  deterministic scores for facts, abstention, schema validity, and rubric criteria.
  Add hallucination/factuality and prompt regressions, model/prompt comparisons, and
  repeated-run reliability results. Emit JSON case results and denominators.
- **Dependencies/cost:** start with standard Python and pytest; add one optional
  provider SDK only when needed. Offline evaluation has no provider cost. Live runs
  need explicit request/token/cost limits and credentials outside Git.
- **Acceptance/claims:** versioned reviewed data, clear scoring tests, reproducible
  reports, and a demonstrated controlled assistant are required before claiming an
  evaluation harness. Provider/model claims require actual recorded live runs.
  Optional LLM-as-judge scoring comes after human calibration and agreement checks;
  never present judge scores as deterministic truth.

## Stage 3 — Agentic QA (future)

- **Objective/career relevance:** demonstrate testing of agent decisions and permission
  boundaries, including multi-turn behavior, rather than unrestricted autonomy.
- **Architecture:** a small allowlisted API tool adapter, argument schemas, permission
  checks, approval decisions, and bounded step count. Begin read-only. Any optional
  state-changing operation must require explicit approval and owned synthetic IDs;
  provide no unrestricted SQL or database-mutation tool.
- **Reuse/files:** `ApiClient`, contracts, synthetic data, and manager cleanup;
  proposed `src/ai_lab/tools.py`, `src/ai_lab/permissions.py`, and `tests/agent/`.
- **Testing:** expected tool selection/arguments, response interpretation, unauthorized
  calls, read/write distinctions, approval denial, multi-step completion, missing or
  incorrect data, tool failures/recovery, and injection in tool responses. Compare
  expected and observed call sequences using scripted offline responses, then separate
  bounded live runs.
- **Dependencies/cost:** ordinary Python adapters first; no orchestration platform
  unless the small implementation demonstrates a need. Live multi-step runs have
  explicit step, token, request, latency, and cost budgets.
- **Acceptance/claims:** denied actions must demonstrably stay unexecuted; trace tests
  must show both successful tasks and controlled recovery/permission failures. Agentic
  testing claims require these executable scenarios and actual trace evidence.

## Stage 4 — RAG and AI security (future)

- **Objective/career relevance:** demonstrate retrieval evaluation, answer grounding,
  hallucination checks, and bounded AI security testing.
- **Architecture:** separate retriever, answer generator, and scorer over a small
  fictional product/support/returns corpus. Fictional return policies require their
  own reviewed specification; do not add them to the existing order baseline.
- **Reuse/files:** Python testing and synthetic fixtures; proposed `knowledge/`,
  `src/ai_lab/retrieval.py`, `tests/retrieval/`, and `tests/ai_security/`.
- **Testing:** label relevant document sets so precision/recall are measurable; test
  relevant retrieval, source references, grounded versus unsupported claims, missing
  information, contradictions, injected instructions, and document-update regressions.
  Score retrieval separately from generated answers. Add synthetic disclosure canaries,
  excessive-permission/unauthorized-call cases, failure handling, model-output validation,
  and structured-output contract violations.
- **Dependencies/cost:** start with local lexical retrieval and fixtures; justify
  embeddings/vector storage only if the scenarios need them. Live generation or
  embedding costs remain optional and budgeted.
- **Acceptance/claims:** reviewed relevance labels, runnable retrieval/grounding tests,
  sanitized adversarial evidence, and explicit limitations. A small local scenario
  set does not constitute a comprehensive security assessment or certification.

Security scenarios should be mapped to the edition actually reviewed at implementation
time. The [OWASP GenAI initiative](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/)
currently links the 2026 guide (checked 2026-11-13). Prompt injection, sensitive-data
disclosure, excessive agency, and unsafe output handling inform the proposed scope;
this branch implements none of those AI-specific security tests. Preserve the selected
reference edition in future reports rather than assuming category numbers stay fixed.

## Stage 5 — CI/CD and portfolio evidence (future)

- **Objective/career relevance:** demonstrate reproducible AI evaluation gates and
  reporting that a reviewer can independently assess.
- **Architecture:** extend existing GitHub Actions with an offline deterministic
  evaluation job; separate opt-in live-model execution with explicit credentials,
  allowed providers, cost controls, and sanitized logs. Keep software regression
  runnable without provider network access or AI keys.
- **Reuse/files:** existing workflow/report conventions; proposed evaluation job,
  `scripts/run_evaluations.py`, and ignored `artifacts/evaluation/` reports. Version
  datasets and prompts alongside reviewed threshold changes.
- **Testing/reporting:** test scoring and report schemas; compare versioned baselines
  and regression differences. Record case/dataset/prompt/model versions, expected and
  observed outcomes, scores, failure class, tool sequence, latency, human decisions,
  and token/cost data where the provider supports them. Mark unavailable metrics
  explicitly. Separate deterministic and nondeterministic results.
- **Dependencies/cost:** use JSON/JUnit and existing artifact upload first. No large
  observability platform is needed for a small lab. Live CI needs approved budgets
  and secrets configuration; deterministic CI must remain the default.
- **Acceptance/claims:** documented pass/fail thresholds, demonstrated failing and
  passing regressions, retained reports, and an actual hosted run linked to its commit.
  CI/evaluation resume claims wait for that evidence and final quality review.

## Optional research after the core stages

Prioritize MCP tool integration/contract tests when an actual tool is needed; deeper
multi-turn evaluation and judge-agreement studies after stable datasets; provider
comparisons after comparable runs; performance/load fundamentals after workload and
budget definitions; cloud testing after a hosting need; accessibility testing after
an AI interface exists. Each needs a scoped proposal, acceptance criteria, costs,
and review before implementation. Do not add technologies merely to list keywords,
train models, or imply production-scale platform experience.

## Interview evidence

For each completed stage, explain what was built, why this architecture fits, how AI
assisted, how outputs were independently checked, which real defects or coverage gaps
were found, exact execution/results, and remaining limits. Link the relevant code,
owner decisions, and dated reports. Label personal-project work separately from
professional QA employment; do not manufacture dates, metrics, responsibilities,
historical AI errors, or human approvals.
