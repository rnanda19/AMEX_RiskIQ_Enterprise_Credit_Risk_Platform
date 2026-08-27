# Build context is src/ itself -- this service is fully self-contained (the real frozen policy
# JSON ships alongside the code, no separate models/ folder needed). Build manually with:
#     docker build -f docker/Dockerfile -t amex-ews-api .
# run from 07_Problem7_Early_Warning_System/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY real_time_alert_service.py .
COPY early_warning_deployment_policy.json .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8007

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8007/health', timeout=3)" || exit 1

CMD ["uvicorn", "real_time_alert_service:app", "--host", "0.0.0.0", "--port", "8007"]
