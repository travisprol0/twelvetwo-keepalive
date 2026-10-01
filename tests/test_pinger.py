import os
from unittest.mock import patch

import pytest

from keepalive.pinger import PingResult, load_config, ping


def test_load_config_reads_url_and_interval(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https://twelvetwo.onrender.com/")
    monkeypatch.setenv("INTERVAL_MINUTES", "12")

    config = load_config()

    assert config.url == "https://twelvetwo.onrender.com/"
    assert config.interval_minutes == 12


def test_load_config_defaults_to_ten_minutes(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https://twelvetwo.onrender.com/")
    monkeypatch.delenv("INTERVAL_MINUTES", raising=False)

    config = load_config()

    assert config.interval_minutes == 10


def test_load_config_rejects_non_positive_interval(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https://twelvetwo.onrender.com/")
    monkeypatch.setenv("INTERVAL_MINUTES", "0")

    with pytest.raises(ValueError, match="INTERVAL_MINUTES"):
        load_config()


def test_load_config_requires_target_url(monkeypatch):
    monkeypatch.delenv("TARGET_URL", raising=False)

    with pytest.raises(ValueError, match="TARGET_URL"):
        load_config()


def test_ping_returns_status_from_the_site():
    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b"ok"

    with patch("keepalive.pinger.urlopen", return_value=FakeResponse()) as opened:
        result = ping("https://twelvetwo.onrender.com/", timeout_seconds=20)

    assert result == PingResult(url="https://twelvetwo.onrender.com/", status=200, ok=True)
    opened.assert_called_once()
    request = opened.call_args.args[0]
    assert request.full_url == "https://twelvetwo.onrender.com/"
    assert opened.call_args.kwargs["timeout"] == 20
