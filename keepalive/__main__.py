import logging
import time

from keepalive.pinger import load_config, ping

log = logging.getLogger("keepalive")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config()
    log.info(
        "pinging %s every %s minutes (timeout %ss)",
        config.url,
        config.interval_minutes,
        config.timeout_seconds,
    )
    while True:
        result = ping(config.url, timeout_seconds=config.timeout_seconds)
        if result.ok:
            log.info("%s %s", result.status, result.url)
        else:
            log.warning("ping failed status=%s url=%s", result.status, result.url)
        time.sleep(config.interval_minutes * 60)


if __name__ == "__main__":
    main()
