FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY risk_tier_service.py .

RUN useradd --create-home --uid 1000 amexrisktier && chown -R amexrisktier:amexrisktier /app
USER amexrisktier

ENV AMEX_PROJECT_ROOT=/mnt/amex-project

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health', timeout=3)" || exit 1

CMD ["uvicorn", "risk_tier_service:app", "--host", "0.0.0.0", "--port", "8001"]
