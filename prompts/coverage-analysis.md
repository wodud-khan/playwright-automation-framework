# Coverage analysis

Inputs: approved requirements and decision table; current executable test functions;
latest validation evidence; feature scope and risk priorities.

Follow `AGENTS.md`. Compare acceptance criteria with assertions, not filenames or
test counts. Identify boundary values, invalid/valid partitions, missing fields,
normalization, and cross-layer risks where applicable. Distinguish executable source
coverage from cases actually run in the required environment. Treat SQLite and mocked
responses according to their limited scope.

Output: requirement ID, existing file/function evidence, missing behavior, risk,
proposed test, value, and add/defer decision. Identify redundant proposals while
preserving existing working tests. Keep requirements separate from assumptions;
obtain human verification of prioritization and unapproved policies before generation.
Do not add every candidate automatically or introduce coverage frameworks unnecessarily.
