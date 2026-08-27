# Build context is src/ itself -- this service ships its own small, self-contained real
# policy artifacts (no separate models/ folder needed at build time). Build manually with:
#     docker build -f docker/Dockerfile -t amex-p10-api .
# run from Problem10_Credit_Line_Management/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY credit_line_scoring_service.py .
COPY credit_line_deployment_policy.json .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8010/health', timeout=3)" || exit 1

CMD ["uvicorn", "credit_line_scoring_service:app", "--host", "0.0.0.0", "--port", "8010"]
