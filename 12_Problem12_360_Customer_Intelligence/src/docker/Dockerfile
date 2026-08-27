# Build context is src/ itself -- this service ships its own small, self-contained real
# policy artifacts (no separate models/ folder needed at build time). Build manually with:
#     docker build -f docker/Dockerfile -t amex-p12-api .
# run from 12_Problem12_360_Customer_Intelligence/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY customer_intelligence_lookup_service.py .
COPY customer_intelligence_deployment_policy.json .

# NOTE: this service also needs the real, non-committed per-customer profile parquet
# (see ../data/README.md) -- mount it at runtime (see docker-compose.yml's volumes:),
# it is deliberately NOT baked into this image.

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8012

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8012/health', timeout=3)" || exit 1

CMD ["uvicorn", "customer_intelligence_lookup_service:app", "--host", "0.0.0.0", "--port", "8012"]
