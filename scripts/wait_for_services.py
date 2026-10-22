"""Wait for an HTTP readiness endpoint with a bounded timeout."""

from __future__ import annotations

import argparse
import os
import time
from math import isfinite
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def wait_for_url(url: str, timeout_seconds: float, interval_seconds: float = 0.25) -> None:
    """Poll an HTTP endpoint until it succeeds or the bounded timeout expires."""
    if not isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("Timeout must be finite and greater than zero")
    if not isfinite(interval_seconds) or interval_seconds <= 0:
        raise ValueError("Interval must be finite and greater than zero")
    deadline = time.monotonic() + timeout_seconds
    last_error = "no response"

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        try:
            with urlopen(url, timeout=min(2, remaining)) as response:
                if 200 <= response.status < 300:
                    return
                last_error = f"HTTP {response.status}"
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = str(error)
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(interval_seconds, remaining))

    raise TimeoutError(f"{url} was not ready within {timeout_seconds}s: {last_error}")


def main() -> None:
    """Parse command-line options and wait for service readiness."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default=os.getenv("APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/") + "/health",
        help="Readiness URL to poll",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30,
        help="Maximum number of seconds to wait",
    )
    arguments = parser.parse_args()
    wait_for_url(arguments.url, arguments.timeout)
    print(f"Ready: {arguments.url}")


if __name__ == "__main__":
    main()
