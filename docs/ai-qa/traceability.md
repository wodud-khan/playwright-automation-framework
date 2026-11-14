# Requirements to executable tests

The [baseline](order-requirements.md) is owner-approved for the demonstration.
Coverage below describes assertions in source. Execution status is recorded separately
in [validation](validation.md); a listed test is not evidence of a passing run by itself.

| ID | Test file and function | Coverage and remaining gaps |
|---|---|---|
| ORD-001 | [`tests/api/test_orders_api.py`](../../tests/api/test_orders_api.py): `test_create_order_rejects_missing_required_field`, `test_create_order_rejects_invalid_input`; [`tests/unit/test_schemas.py`](../../tests/unit/test_schemas.py): `test_order_input_rejects_invalid_business_values` | New four-field omission cases; existing extra-field rejection. Null/type policy deferred. |
| ORD-002 | [`test_schemas.py`](../../tests/unit/test_schemas.py): `test_order_input_accepts_name_length_boundaries`, `test_order_input_rejects_invalid_business_values`; API `test_create_order_rejects_invalid_input` | New accepted 2/80 cases for each name; complementary unit 1/81 rejection. Explicit padded-80 rejection and empty strings remain gaps. |
| ORD-003 | [`test_schemas.py`](../../tests/unit/test_schemas.py): `test_order_input_normalizes_human_text`; [`tests/unit/test_database.py`](../../tests/unit/test_database.py): `test_repository_round_trip_uses_exact_order_id` | Both-name trimming/internal spaces checked in unit input; normalized customer in SQLite round trip. API/PostgreSQL normalization not directly asserted. |
| ORD-004 | API `test_create_order_accepts_numeric_boundaries`, `test_create_order_rejects_invalid_input`; unit `test_order_input_rejects_invalid_business_values` | New accepted 1/100; existing 0/101 rejection. |
| ORD-005 | Same three functions as ORD-004 | New accepted 1/1,000,000 cents; existing 0/1,000,001 rejection. |
| ORD-006 | API `test_create_order_accepts_numeric_boundaries`, `test_create_and_read_order`; [`tests/e2e/test_order_workflow.py`](../../tests/e2e/test_order_workflow.py): `test_ui_order_is_visible_through_api_and_postgresql` | New four literal boundary totals; existing independent 4998, 2499, and 7497 totals. |
| ORD-007 | API `test_create_and_read_order`, `test_create_order_accepts_numeric_boundaries`; [`tests/contract/test_order_contract.py`](../../tests/contract/test_order_contract.py): `test_create_and_read_responses_match_order_contract` | 201 checked by manager; GET 200 and body equality in API tests; independent contract checks retained. |
| ORD-008 | API `test_create_order_rejects_missing_required_field`, `test_create_order_rejects_invalid_input`, `test_unknown_order_returns_not_found`, `test_delete_unknown_order_returns_not_found`; contract `test_validation_error_matches_contract`, `test_not_found_matches_error_contract` | Missing-field details now checked; existing invalid-input 422 and exact not-found body checks. |
| ORD-009 | [`tests/database/test_order_persistence.py`](../../tests/database/test_order_persistence.py): `test_created_order_is_persisted_with_exact_values`; E2E workflow above | Existing exact SQL values at ordinary inputs; numeric extremes are API evidence, not direct SQL boundary coverage. |
| ORD-010 | [`tests/integration/test_order_lifecycle.py`](../../tests/integration/test_order_lifecycle.py): `test_api_create_and_delete_are_reflected_in_postgresql`; E2E workflow; [`tests/e2e/test_failure_cleanup.py`](../../tests/e2e/test_failure_cleanup.py): `test_ui_created_order_is_removed_after_result_assertion_fails`; [`tests/unit/test_framework_components.py`](../../tests/unit/test_framework_components.py): `test_order_manager_cleans_up_only_its_exact_order`, `test_unexpected_create_status_registers_only_api_verified_order`, `test_unexpected_create_status_does_not_claim_unrelated_order`, `test_order_manager_uses_explicit_payload_without_building_another` | Existing exact-ID/absence and failure-path proof; new helper regression preserves supplied payload and ownership. |
| ORD-011 | E2E workflow; [`tests/ui/test_order_page.py`](../../tests/ui/test_order_page.py): `test_customer_name_is_required_before_submission`, `test_validation_feedback_is_readable_and_allows_retry`, `test_mocked_order_failure_shows_feedback`, `test_order_page_exposes_critical_controls` | Existing UI success, required-customer, 422 and mocked 503 feedback. Re-enabling is asserted for 422; re-enabling after success/503 and a subsequent successful retry are not directly asserted. The 503 case is not a real service outage. |

## Selected additions and deferred gaps

Owner approved the first three groups on 2026-11-13. The helper adjustment supports
those tests; it is not a new product requirement. Codex's final engineering review is
complete; personal owner review of the generated code has not occurred.

| IDs | Existing evidence / missing coverage | Risk | Proposed test and value | Decision |
|---|---|---|---|---|
| ORD-004–007 | Ordinary creation/totals and invalid limits; no accepted extremes | Inclusive limits or total calculation can be wrong while rejection tests pass | Four-corner API test with literal totals and GET equality | Added |
| ORD-001, ORD-008 | Invalid supplied fields; no omissions | Accidental defaults/optional fields can escape detection | Four omissions, exact missing-field location/type | Added |
| ORD-002 | Asymmetric invalid names; no accepted endpoints | Off-by-one or field-specific constraint regression | Four accepted unit endpoints; three missing negative cases added to existing test | Added |
| ORD-010 | Manager previously built only default data | Raw POST in new tests would duplicate creation/ownership handling | Optional typed payload on existing manager; one focused helper regression | Added after AI review; owner code review pending |
| ORD-003 | Unit trimming and SQLite customer persistence; no normalized API/SQL assertions | Normalization may differ across layers | Focused future API normalization test | Deferred; lower priority for this batch |
| ORD-002 | Validation order inspected; padded length/empty string not directly tested | Misunderstood raw-length contract | Future padded 80-character name rejection and empty cases | Deferred to keep selected scope small |
| ORD-009 | Existing ordinary SQL value checks | Boundary values not independently read through SQL | Future direct SQL boundary check if risk warrants it | Deferred; no SQL boundary claim |
| ORD-004–006 | Four corners selected; existing 0/101 and price rejection cases | Redundant tests increase maintenance | Additional copies across unit/UI/SQL or all integer combinations | Not added; retain existing layer-specific tests |

Test-instance counts measure executed cases only. They are not a percentage of business
coverage. No existing working tests were removed.
