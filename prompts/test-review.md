# Test review

Inputs: complete diff; approved requirements; existing helper/fixture implementations;
available command output and failure artifacts.

Review the entire diff under `AGENTS.md`. Check expected values, boundaries, missed
negative cases, locators, invented rules, redundant tests, collisions, fixture scope,
ownership/cleanup, flakiness, naming, complexity, and documentation accuracy. Distinguish
code inspection from executed validation. Preserve working code unless a concrete
improvement warrants change. Never weaken assertions just to pass.

Output: findings with requirement ID, file/function, evidence, impact, recommended
correction, actual change if authorized, and retest status. Record real findings in
`docs/ai-qa/ai-review-log.md` or the feature's equivalent. Say honestly when no issue
was found. Separate approved requirements, assumptions, AI review, and pending human
code review. Do not fabricate owner approval, past failures, or test results. Prefer
existing helpers to new wrappers or dependencies.
