"""Readiness polling respects configuration and a finite wait budget."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests

from scripts import wait_for_services


@pytest.mark.unit
def test_readiness_uses_remaining_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wait_for_services.time, "monotonic", Mock(side_effect=[0, 0.8, 1.1, 1.1]))
    sleep = Mock()
    monkeypatch.setattr(wait_for_services.time, "sleep", sleep)
    request = Mock(side_effect=requests.ConnectionError("offline"))
    monkeypatch.setattr(wait_for_services.requests, "get", request)

    with pytest.raises(TimeoutError, match="offline"):
        wait_for_services.wait_for_url("http://localhost/health", 1)

    assert request.call_args.kwargs["timeout"] == pytest.approx(0.2)
    sleep.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://localhost", "http:///health"])
def test_readiness_rejects_non_http_urls(url: str) -> None:
    with pytest.raises(ValueError, match="absolute HTTP"):
        wait_for_services.wait_for_url(url, 1)


@pytest.mark.unit
@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_readiness_rejects_invalid_budget(timeout: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        wait_for_services.wait_for_url("http://localhost/health", timeout)


@pytest.mark.unit
def test_readiness_cli_uses_app_url_and_explicit_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_BASE_URL", "http://localhost:8080/")
    wait = Mock()
    monkeypatch.setattr(wait_for_services, "wait_for_url", wait)
    monkeypatch.setattr("sys.argv", ["wait_for_services.py"])
    wait_for_services.main()
    wait.assert_called_with("http://localhost:8080/health", 30)

    monkeypatch.setattr(
        "sys.argv", ["wait_for_services.py", "--url", "http://localhost:9000/health"]
    )
    wait_for_services.main()
    wait.assert_called_with("http://localhost:9000/health", 30)
