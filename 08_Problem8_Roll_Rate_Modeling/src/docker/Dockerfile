# Build context is src/ itself -- this service is fully self-contained (the real frozen policy
# JSON ships alongside the code, no separate models/ folder needed). Build manually with:
#     docker build -f docker/Dockerfile -t amex-rr-api .
# run from 08_Problem8_Roll_Rate_Modeling/src/ itself, or use docker-compose.yml.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY roll_rate_scoring_service.py .
COPY roll_rate_deployment_policy.json .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8005/health', timeout=3)" || exit 1

CMD ["uvicorn", "roll_rate_scoring_service:app", "--host", "0.0.0.0", "--port", "8005"]
