# Requirements analysis

Inputs: supplied specification and its approval status; relevant implementation,
tests, and known ambiguities; requested feature scope.

Read `AGENTS.md` and the affected source/tests before analysis. Use
`docs/ai-qa/order-requirements.md` as the format example, not as requirements for
another feature. Assign stable IDs and measurable acceptance criteria. Separate
explicit requirements from implementation observations and proposed assumptions.
Identify positive, negative, boundary, and equivalence scenarios. Flag material
conflicts and unanswered policies for owner review; do not invent business rules.

Output: a concise requirement table with source, approval status, acceptance criteria,
candidate scenarios, and owner questions. Stop dependent test generation until material
assumptions are resolved. Human verification is required before treating reconstructed
rules as approved expectations. Keep the existing stack and dependencies.
