# Build context is src/ itself -- this service ships its own small, self-contained real
# policy artifacts (no separate models/ folder needed at build time). Build manually with:
#     docker build -f docker/Dockerfile -t amex-p11-api .
# run from Problem11_Real_Time_Portfolio_Monitoring/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY portfolio_alert_feed_service.py .
COPY portfolio_monitoring_deployment_policy.json .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8011

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8011/health', timeout=3)" || exit 1

CMD ["uvicorn", "portfolio_alert_feed_service:app", "--host", "0.0.0.0", "--port", "8011"]
