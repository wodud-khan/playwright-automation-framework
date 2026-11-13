# Order input decisions and test design

Scope: [approved baseline](order-requirements.md). These tables organize scenarios;
they do not imply every row has an executed test. Refer to [traceability](traceability.md)
and [validation](validation.md) for coverage and run evidence.

## Decisions

Rows are evaluated with unrelated fields valid. When several fields are invalid,
error ordering is not specified here. Numeric-type coercion is outside this table.

| Rule | Required fields | Extra field | Names: raw 2–80 and trimmed >=2 | Quantity 1–100 | Price 1–1,000,000 | API expectation | IDs |
|---|---|---|---|---|---|---|---|
| D1 | All present | No | Valid | Valid | Valid | 201; normalized names and independent total | ORD-001–007 |
| D2 | One missing | No | Otherwise valid | Otherwise valid | Otherwise valid | 422; missing field identified | ORD-001, ORD-008 |
| D3 | All present | Yes | Valid | Valid | Valid | 422; extra field identified | ORD-001, ORD-008 |
| D4 | All present | No | Invalid | Valid | Valid | 422; affected name identified | ORD-002, ORD-008 |
| D5 | All present | No | Valid | Invalid | Valid | 422; quantity identified | ORD-004, ORD-008 |
| D6 | All present | No | Valid | Valid | Invalid | 422; unit price identified | ORD-005, ORD-008 |

| Lifecycle decision | Expected result | IDs |
|---|---|---|
| GET an existing ID | 200; same representation as creation; SQL values agree | ORD-007, ORD-009 |
| DELETE an existing owned ID | 204, then GET 404 and SQL absence | ORD-010 |
| GET or DELETE an unknown ID | 404 with `Order not found` detail | ORD-008 |
| UI receives success / validation error / mocked 503 | Saved values / readable field error / readable service error; retry control enabled where asserted | ORD-011 |

## Boundary values and equivalence partitions

| Input | Valid partition and boundary scenarios | Invalid partitions and scenarios | Selection |
|---|---|---|---|
| Each name | Raw length 2–80, trimmed length >=2; exact lengths 2 and 80 | Empty, length 1, raw length 81+, or trimmed length <2 | Add both accepted endpoints for each field; extend existing unit rejection cases for uncovered 1/81 values. Existing whitespace cases cover some trimming rejection. Empty-string cases deferred. |
| Surrounding whitespace | Padded names within the raw limit normalize; internal text preserved | Whitespace-only or raw >80 even if trimmed value fits | Existing unit normalization and SQLite customer round trip; API normalization and padded-limit cases deferred. |
| Quantity | Integers 1–100; 1, ordinary 2/3, and 100 | Below/above range: 0, 101 | Existing rejection cases; add accepted API extremes. |
| Unit price | Integers 1–1,000,000; 1, ordinary 2499, and 1,000,000 | Below/above range: 0, 1,000,001 | Existing rejection cases; add accepted API extremes. |
| Field presence | All four supplied | Each single omission; unknown additional field | Add four single-omission API cases; retain existing extra-field cases. |

The selected boundary-total cases use literal oracles rather than application helpers:

| Quantity | Unit price (cents) | Expected total (cents) |
|---|---|---|
| 1 | 1 | 1 |
| 100 | 1 | 100 |
| 1 | 1,000,000 | 1,000,000 |
| 100 | 1,000,000 | 100,000,000 |

These four corners test independent numeric limits and their interaction. They do not
establish coverage of every integer or every input type. No full Cartesian product of
names, prices, quantities, browsers, and validation failures is proposed.
