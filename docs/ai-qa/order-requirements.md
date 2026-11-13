# Order Lab demonstration requirements

Baseline: `92df19f146908a0e38ad9d633f4c596137463d25`.
On 2026-11-13 the repository owner approved ORD-001–011 and the three selected
test groups after Codex source inspection. These are approved expectations for the
controlled portfolio application, not requirements from an external business owner.
Approval covers the baseline and scenarios; the resulting code still awaits personal
owner review. No application behavior is changed by this work.

## Source inspection inventory, before edits

| Classification | Evidence or opportunity |
|---|---|
| Implemented and demonstrated in existing test code | API create/read, invalid numeric limits, ordinary totals, trimming, independent JSON contracts, PostgreSQL reads/deletion, UI feedback, and controlled failure-cleanup drills. This inventory did not itself execute tests. |
| Implemented but not formally documented | Required fields, exact name-validation order, inclusive numeric limits, and extra-field rejection had no stable requirement IDs or acceptance-criteria mapping. |
| Partially covered | Valid numeric/name extremes, missing API fields, API normalization, and boundary totals. |
| Missing | Repository agent instructions, reusable design/review prompts, decision tables, requirement traceability, and a proposal-to-validation review record. |
| Ambiguous at inspection | Name-validation order and numeric coercion policy. Owner subsequently approved preserving validation-before-trimming; coercion policy remains unresolved. |

## Approved acceptance criteria

Each criterion applies to otherwise valid input. Error cases change one factor unless
explicitly testing a combination. See the [decision table](decision-table.md) for
partitions and the [traceability matrix](traceability.md) for executable test references.

| ID | Acceptance criteria | Implementation source |
|---|---|---|
| ORD-001 | POST input requires `customer_name`, `item_name`, `quantity`, and `unit_price_cents`. Missing fields and additional fields are rejected with 422. | [`OrderCreate`](../../src/demo_app/schemas.py), `create_order` in [`main.py`](../../src/demo_app/main.py) |
| ORD-002 | Both submitted names must be 2–80 characters inclusive **before trimming**. After trimming, at least two characters must remain. | `OrderCreate` field constraints and `strip_text` |
| ORD-003 | Strip surrounding whitespace from both names and preserve internal text. Returned and persisted names use normalized values. | `strip_text`, [`OrderRepository.create`](../../src/demo_app/repository.py) |
| ORD-004 | Accept integer quantities 1–100 inclusive; reject 0 and 101 with 422. | `OrderCreate.quantity` |
| ORD-005 | Accept integer unit prices 1–1,000,000 cents inclusive; reject 0 and 1,000,001 with 422. | `OrderCreate.unit_price_cents` |
| ORD-006 | Response total in cents equals quantity multiplied by unit price. Use independently specified expected totals, including numeric extremes. | `OrderResponse.from_record` in [`schemas.py`](../../src/demo_app/schemas.py) |
| ORD-007 | POST `/api/orders` returns 201 and a representation of the created order. GET that exact ID returns 200 and the same representation. | `create_order`, `get_order` |
| ORD-008 | Invalid order input returns 422 with field-level validation details. GET/DELETE of an unknown order returns 404 and `{"detail":"Order not found"}`. | `OrderCreate`, `get_order`, `delete_order` |
| ORD-009 | Created order ID, names, quantity, unit price, and status agree with the exact PostgreSQL row. `total_cents` is derived, not a stored column. | [`OrderRepository`](../../src/demo_app/repository.py), [`database.py`](../../src/demo_app/database.py) |
| ORD-010 | DELETE of an existing order returns 204; subsequent GET returns 404 and direct PostgreSQL lookup finds no row for that ID. Test cleanup addresses only owned IDs and verifies absence. | `delete_order`, `OrderRepository.delete`, [`OrderManager`](../../src/test_framework/order_manager.py) |
| ORD-011 | UI uses fixed price 2499 cents, displays the saved ID/status/total and `Order saved.`; required-field blocking and readable validation/error feedback are available. Submission becomes enabled after completion/failure. | [`index.html`](../../src/demo_app/static/index.html), [`app.js`](../../src/demo_app/static/app.js), [`OrderPage`](../../src/test_framework/pages/order_page.py) |

## Boundaries and unresolved policies

Validation-before-trimming is approved for this iteration. An 80-character name padded
with two spaces has submitted length 82 and is rejected even though its trimmed length
is 80. `strip_text` checks trimmed length, not a rule forbidding internal spaces.
No new assertions about Unicode normalization or allowed character sets are authorized.

Pydantic's current coercion behavior is preserved. Whether numeric strings, booleans,
nulls, fractional values, or other types should receive a stricter business policy
remains an owner decision. The new numeric cases use plain integers only.

Further decisions: whether to prioritize API normalization and explicit padded-length
tests; whether to broaden actual UI outage/recovery coverage beyond the existing mocked
503 case. Existing tests do not establish those broader claims. Authentication, return
policies, contact compliance, AI assistant behavior, and future roadmap features are
outside this order baseline.
