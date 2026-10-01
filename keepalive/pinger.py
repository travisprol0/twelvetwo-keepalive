import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_INTERVAL_MINUTES = 10
DEFAULT_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class Config:
    url: str
    interval_minutes: int
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS


@dataclass(frozen=True)
class PingResult:
    url: str
    status: int | None
    ok: bool


def load_config() -> Config:
    url = os.environ.get("TARGET_URL", "").strip()
    if not url:
        raise ValueError("TARGET_URL is required")

    interval = _positive_int(
        os.environ.get("INTERVAL_MINUTES", str(DEFAULT_INTERVAL_MINUTES)),
        "INTERVAL_MINUTES",
    )
    timeout = _positive_int(
        os.environ.get("TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)),
        "TIMEOUT_SECONDS",
    )
    return Config(url=url, interval_minutes=interval, timeout_seconds=timeout)


def ping(url: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> PingResult:
    request = Request(url, method="GET", headers={"User-Agent": "twelvetwo-keepalive"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            response.read()
            status = response.status
    except HTTPError as exc:
        return PingResult(url=url, status=exc.code, ok=False)
    except URLError:
        return PingResult(url=url, status=None, ok=False)
    return PingResult(url=url, status=status, ok=200 <= status < 400)


def _positive_int(raw: str, name: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value
