# AI proposal and review log

Session: 2026-11-13, Codex, branch `feat/ai-assisted-qa-evidence`, baseline `92df19f`.
The owner approved ORD-001–011 and the three test groups in the follow-up request.
That approval does not establish personal review of individual generated assertions
or the final diff. Reviews below are Codex self-review, not an independent human or
second-model review. Execution results are separately recorded in [validation](validation.md).

## Actual proposals and corrections

| Entry / requirement | AI proposal and file/function | Issue identified and recommendation | Approval / actual change | Execution and result |
|---|---|---|---|---|
| R1 / ORD-004–007, ORD-010 | First draft of `test_create_order_accepts_numeric_boundaries` in [`tests/api/test_orders_api.py`](../../tests/api/test_orders_api.py) used a raw POST and registered any response containing `id` before checking 201. | This bypassed the existing manager's non-201 ownership verification. An error response containing an unrelated ID could cause teardown to delete unowned state. This was an actual draft review finding, not an executed product failure. Reuse the manager's creation path. | Scenario group approved; correction awaits owner code review. [`OrderManager.create`](../../src/test_framework/order_manager.py) now accepts an optional typed `OrderData`; default calls retain their behavior. Boundary data uses `dataclasses.replace` and passes through the manager. No new helper class or parallel creation path. | Corrected code: serial service suite 23 passed; two-worker service suite 23 passed. Unit suite 72 passed, including existing verified/unrelated unexpected-status ownership tests and the new supplied-payload regression. Faulty draft was not executed. |
| R2 / ORD-002, ORD-008 | Extend `test_order_input_rejects_invalid_business_values` in [`tests/unit/test_schemas.py`](../../tests/unit/test_schemas.py). | Existing assertion only required any `ValidationError`; an unrelated invalid field could make the test pass. Require the error location to identify the changed field. Add only the three missing name rejection cases, preserving the existing item-length-1 case. | Boundary group approved; individual strengthened assertion awaits owner review. Added exact error-location comparison and complementary customer 1/81 and item 81 cases. | Unit suite: 72 passed serially and 72 passed on two workers. No deliberately incorrect expectation was needed. |
| R3 / ORD-004–007 | Initial formatting of the boundary payload replacement in `test_create_order_accepts_numeric_boundaries`. | Actual `ruff format --check .` failed because one call fit on one line. Apply the existing formatter; do not change behavior. | Owner code review pending. `ruff format tests/api/test_orders_api.py` reformatted one file. | Initial formatting gate failed; subsequent formatting check passed. Lint and Mypy passed. The first static command chain stopped at formatting, so Mypy ran in the subsequent check. |
| R4 / ORD-001, ORD-008 | `test_create_order_rejects_missing_required_field` in [`test_orders_api.py`](../../tests/api/test_orders_api.py): omit each required field and compare exact location plus `missing` error type. | No incorrect expected value or invented coercion policy found during review. Test changes one factor per case and checks HTTP behavior. Keep it in the API layer instead of repeating omissions across all layers. | Group approved; generated assertions await owner review. Four parameterized API cases added. | All four cases passed within both 23-case service runs. |
| R5 / ORD-002, ORD-004–006 | Four numeric corners with literal totals; both names at lengths 2 and 80. Files/functions: API `test_create_order_accepts_numeric_boundaries`; unit `test_order_input_accepts_name_length_boundaries`. | Arithmetic and inclusive endpoints checked against approved criteria. No incorrect numeric oracle, additional character policy, or redundant copy of an existing accepted-endpoint case found. Keep service data unique and fixed short strings unit-only. | Groups approved; final assertions await owner review. Four API and four name-boundary unit cases added. | Passed in serial/two-worker unit and service suites. No application behavior change. |
| R6 / existing CI image-security gate, not a new product requirement | Follow-up Trivy scan of the rebuilt app image; [`Dockerfile`](../../Dockerfile), app stage. | Actual scan failed with 16 HIGH findings in inherited `krb5-libs` 1.22.2-r1; scanner identified 1.22.3-r0 as fixed. Apply the existing database-stage OS patch convention to the app stage. No application exploit was reproduced. | Authorized under autonomous completion and fixing in-scope quality checks; personal owner code review not performed. Added `apk upgrade --no-cache` to the existing app-stage RUN instruction. No advisory suppression or Python dependency change. | Initial app scan exited 1; patched image scan exited 0 with zero HIGH/CRITICAL findings. Database image scan passed. Full suite passed before and after patch: 104 cases each run. Original and corrected reports preserved. |

The helper regression is
[`test_order_manager_uses_explicit_payload_without_building_another`](../../tests/unit/test_framework_components.py).
It verifies the exact POST payload, absence of a second factory build, preservation
of returned payload data, and registered ownership. Existing cleanup tests remain.

## Entire-diff engineering review

Codex reviewed all changed Python and Markdown files, including new untracked documents,
against the source and approved scope. The review checked incorrect values, weak
assertions, missing negatives, boundaries, invented rules, fixture usage, data collisions,
cleanup, flakiness, naming, duplication, complexity, and misleading evidence claims.

- Kept the framework change to one optional typed argument on the existing manager.
  No application rewrite, new dependency, wrapper hierarchy, or new runner was needed.
- Kept independent literal totals. Retained existing layer-specific tests; did not copy
  every input case to UI/SQL or remove working tests to improve results.
- Kept synthetic factory ownership for new service records and native fixture lifecycle.
  New code adds no locators, waits, retries, or browser-event suppressions.
- Corrected a stray `+` joining two sentences in the workflow documentation during
  review. Checked document links, requirement/function references, and separation of
  source coverage from execution. Future modules remain explicitly unimplemented.

No remaining concrete code-quality defect was identified in this diff. This is a
bounded self-review result, not a guarantee or final owner acceptance. Remaining
limitations are policy/coverage choices: numeric coercion is unresolved, API normalization
and padded-length rejection lack dedicated assertions, and future AI evaluation/RAG
capabilities are roadmap-only. Personal owner review of the entire diff and any later
permission to push remain pending. Hosted CI has not run for this branch.

The owner subsequently authorized autonomous completion and local commits. A final
review of the entire change set confirmed that the Dockerfile patch addresses an actual
configured quality-gate failure and follows an existing project pattern. No further
abstraction, test duplication, assertion relaxation, or behavior change was warranted.
Gitleaks history/source scans and both image gates now have actual local evidence.
The completed engineering review is Codex self-review; no human approval is inferred.
