"""Unit tests for order request and response rules."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from demo_app.schemas import OrderCreate


@pytest.mark.unit
def test_order_input_normalizes_human_text() -> None:
    order = OrderCreate(
        customer_name="  Grace Hopper ",
        item_name="  Test Journal ",
        quantity=1,
        unit_price_cents=2499,
    )

    assert order.customer_name == "Grace Hopper"
    assert order.item_name == "Test Journal"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("customer_name", " "),
        ("customer_name", "x"),
        ("customer_name", "x" * 81),
        ("item_name", "x"),
        ("item_name", "x" * 81),
        ("quantity", 0),
        ("quantity", 101),
        ("unit_price_cents", 0),
        ("unit_price_cents", 1_000_001),
        ("extra", "unrecognized"),
    ],
)
def test_order_input_rejects_invalid_business_values(field: str, value: object) -> None:
    payload: dict[str, object] = {
        "customer_name": "Grace Hopper",
        "item_name": "Test Journal",
        "quantity": 1,
        "unit_price_cents": 2499,
    }
    payload[field] = value

    with pytest.raises(ValidationError) as caught:
        OrderCreate.model_validate(payload)

    assert [error["loc"] for error in caught.value.errors()] == [(field,)]


@pytest.mark.unit
@pytest.mark.parametrize("field", ["customer_name", "item_name"])
@pytest.mark.parametrize("length", [2, 80])
def test_order_input_accepts_name_length_boundaries(field: str, length: int) -> None:
    payload: dict[str, object] = {
        "customer_name": "Synthetic Customer",
        "item_name": "Test Journal",
        "quantity": 1,
        "unit_price_cents": 2499,
    }
    payload[field] = "x" * length

    order = OrderCreate.model_validate(payload)

    assert getattr(order, field) == "x" * length
