# Debug and retest

Inputs: original failure output/artifacts; exact command, revision, environment,
browser and worker count; approved expectation and affected source/test functions.

Follow `AGENTS.md` and `docs/FLAKY_TEST_POLICY.md`. Preserve first-failure evidence.
Reproduce with the same scope; inspect readiness, exact IDs, HTTP exchanges, browser
events, and teardown. Separate observed facts from hypotheses. Classify product,
test, environment, or cleanup failure. Check approved requirements before changing
expected behavior. Do not suppress errors, add blanket retries, reset shared data,
or silently heal locators/assertions. Use existing diagnostics and dependencies.

Output: evidence-backed cause or unresolved hypotheses; minimal correction and its
justification; original-case retest, affected regression results, and remaining risks.
Record exact commands and pass/fail/not-run outcomes in a dated validation entry.
Request human verification for changed expectations and mark final review pending;
AI investigation is not owner approval. Review artifacts before sharing externally.
