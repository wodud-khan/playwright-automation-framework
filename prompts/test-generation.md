# Test generation

Inputs: approved specification with IDs; selected coverage gaps; existing test files,
fixtures, helpers, and environment constraints.

Read `AGENTS.md` and nearby tests. Generate only the selected scenarios at the
appropriate pytest layer. Reuse factory data, `OrderManager`, clients, and `OrderPage`
where relevant. Preserve exact-ID cleanup and register externally created IDs before
assertions. Use semantic browser locators and observable waits. Keep assertions
independent of application calculations and models used to implement the behavior.

Output: a small typed Python diff, requirement-to-test mapping, independent expected
values, and proposed execution commands. List assumptions separately and leave unresolved
policies unasserted. Mark generated code as awaiting human review; do not claim execution
or approval. Add no runner, agent runtime, or dependency without a demonstrated need.
