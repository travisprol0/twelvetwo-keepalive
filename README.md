Pings the Twelve Two site on an interval so the free Render service stays awake.

Render sleeps a free web service after about 15 minutes with no traffic. Keep `INTERVAL_MINUTES` under 14. The first request after sleep can take a minute or more, so `TIMEOUT_SECONDS` defaults to 120.

```bash
cp .env.example .env
docker compose up -d --build
docker compose logs -f
```

Tests:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest
```
