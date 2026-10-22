"""JSON Schema validation independent of application model classes."""

from __future__ import annotations

import json
from importlib.resources import files

from jsonschema import Draft202012Validator, FormatChecker

SCHEMAS = files("test_framework").joinpath("schemas")


def load_order_schema() -> dict[str, object]:
    return load_schema("order.schema.json")


def load_schema(name: str) -> dict[str, object]:
    """Read a bundled contract from either a checkout or an installed package."""
    schema: dict[str, object] = json.loads(SCHEMAS.joinpath(name).read_text(encoding="utf-8"))
    return schema


def validate_contract(instance: object, schema: dict[str, object]) -> None:
    """Validate one response and raise a detailed schema error on mismatch."""
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    validator.validate(instance)
