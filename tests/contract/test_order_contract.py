"""Black-box JSON Schema checks for order responses."""

from __future__ import annotations

import pytest

from test_framework.api.client import ApiClient
from test_framework.contracts import load_order_schema, load_schema, validate_contract
from test_framework.data_factory import OrderFactory
from test_framework.order_manager import OrderManager


@pytest.mark.contract
def test_create_and_read_responses_match_order_contract(
    order_manager: OrderManager,
    api_client: ApiClient,
) -> None:
    created = order_manager.create()
    validate_contract(created.response_body, load_order_schema())

    read_response = api_client.get(f"/orders/{created.id}")

    assert read_response.status_code == 200
    validate_contract(read_response.json(), load_order_schema())


@pytest.mark.contract
def test_validation_error_matches_contract(
    api_client: ApiClient, order_factory: OrderFactory
) -> None:
    payload = order_factory.build().as_payload()
    payload["quantity"] = 0
    response = api_client.post("/orders", payload)

    assert response.status_code == 422
    validate_contract(response.json(), load_schema("error.schema.json"))


@pytest.mark.contract
def test_not_found_matches_error_contract(api_client: ApiClient) -> None:
    response = api_client.get("/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    validate_contract(response.json(), load_schema("error.schema.json"))
