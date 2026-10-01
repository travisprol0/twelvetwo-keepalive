FROM python:3.12-alpine

WORKDIR /app
COPY keepalive ./keepalive

USER nobody
CMD ["python", "-m", "keepalive"]
