# Build context is src/ itself -- this service ships its own small, self-contained real
# policy artifacts (no separate models/ folder needed at build time). Build manually with:
#     docker build -f docker/Dockerfile -t amex-p13-api .
# run from 13_Problem13_Risk_Adjusted_Profitability_Modeling/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY profitability_scoring_lookup_service.py .
COPY profitability_deployment_policy.json .

# NOTE: this service also needs the real, non-committed per-customer profile parquet
# (see ../data/README.md) -- mount it at runtime (see docker-compose.yml's volumes:),
# it is deliberately NOT baked into this image.

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8013

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8013/health', timeout=3)" || exit 1

CMD ["uvicorn", "profitability_scoring_lookup_service:app", "--host", "0.0.0.0", "--port", "8013"]
