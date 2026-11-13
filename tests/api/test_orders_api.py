"""Black-box REST behavior for the controlled order API."""

from __future__ import annotations

from dataclasses import replace

import pytest

from test_framework.api.client import ApiClient
from test_framework.data_factory import OrderFactory
from test_framework.order_manager import OrderManager


@pytest.mark.api
def test_create_and_read_order(order_manager: OrderManager, api_client: ApiClient) -> None:
    created = order_manager.create()

    assert created.response_body["customer_name"] == created.payload.customer_name
    assert created.response_body["item_name"] == created.payload.item_name
    assert created.response_body["total_cents"] == 4998

    response = api_client.get(f"/orders/{created.id}")

    assert response.status_code == 200
    assert response.json() == created.response_body


@pytest.mark.api
@pytest.mark.parametrize(
    ("quantity", "unit_price_cents", "expected_total_cents"),
    [(1, 1, 1), (100, 1, 100), (1, 1_000_000, 1_000_000), (100, 1_000_000, 100_000_000)],
)
def test_create_order_accepts_numeric_boundaries(
    api_client: ApiClient,
    order_factory: OrderFactory,
    order_manager: OrderManager,
    quantity: int,
    unit_price_cents: int,
    expected_total_cents: int,
) -> None:
    payload = replace(order_factory.build(), quantity=quantity, unit_price_cents=unit_price_cents)
    created = order_manager.create(payload)
    body = created.response_body

    assert body["customer_name"] == payload.customer_name
    assert body["item_name"] == payload.item_name
    assert body["quantity"] == quantity
    assert body["unit_price_cents"] == unit_price_cents
    assert body["total_cents"] == expected_total_cents

    read_response = api_client.get(f"/orders/{body['id']}")
    assert read_response.status_code == 200
    assert read_response.json() == body


@pytest.mark.api
@pytest.mark.parametrize("field", ["customer_name", "item_name", "quantity", "unit_price_cents"])
def test_create_order_rejects_missing_required_field(
    api_client: ApiClient,
    order_factory: OrderFactory,
    field: str,
) -> None:
    payload = order_factory.build().as_payload()
    del payload[field]

    response = api_client.post("/orders", payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert [(error["loc"], error["type"]) for error in errors] == [(["body", field], "missing")]


@pytest.mark.api
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("quantity", 0),
        ("quantity", 101),
        ("unit_price_cents", 0),
        ("unit_price_cents", 1_000_001),
        ("customer_name", "  "),
        ("item_name", "x" * 81),
        ("unexpected", "field"),
    ],
)
def test_create_order_rejects_invalid_input(
    api_client: ApiClient,
    order_factory: OrderFactory,
    field: str,
    value: object,
) -> None:
    payload = order_factory.build().as_payload()
    payload[field] = value

    response = api_client.post("/orders", payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


@pytest.mark.api
def test_unknown_order_returns_not_found(api_client: ApiClient) -> None:
    response = api_client.get("/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.api
def test_delete_unknown_order_returns_not_found(api_client: ApiClient) -> None:
    response = api_client.delete("/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
