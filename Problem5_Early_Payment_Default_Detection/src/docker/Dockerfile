# Build context is the PROBLEM ROOT (two levels up from this file), not src/ -- this service
# needs both src/ (the API code) and models/ (the real trained artifacts) copied in. See
# docker-compose.yml's `context: ../..`, or build manually with:
#     docker build -f src/docker/Dockerfile -t amex-epd-api .
# run from Problem5_Early_Payment_Default_Detection/ itself.
FROM python:3.11-slim

WORKDIR /app

COPY src/requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY src/early_default_service.py .
COPY models/ ./models/

ENV AMEX_EPD_MODELS_DIR=/app/models

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/health', timeout=3)" || exit 1

CMD ["uvicorn", "early_default_service:app", "--host", "0.0.0.0", "--port", "8002"]
