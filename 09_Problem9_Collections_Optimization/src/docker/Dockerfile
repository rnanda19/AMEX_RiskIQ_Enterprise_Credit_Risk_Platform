# Build context is src/ itself -- this service ships its own small, self-contained real
# policy artifacts (no separate models/ folder needed at build time). Build manually with:
#     docker build -f docker/Dockerfile -t amex-p9-api .
# run from 09_Problem9_Collections_Optimization/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY collections_scoring_service.py .
COPY collections_deployment_policy.json .
COPY collections_propensity_xgboost.joblib .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8009

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8009/health', timeout=3)" || exit 1

CMD ["uvicorn", "collections_scoring_service:app", "--host", "0.0.0.0", "--port", "8009"]
