FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY ecl_calculator.py .
COPY ecl_scoring_bundle.json .
COPY ecl_scoring_service.py .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8003/health', timeout=3)" || exit 1

CMD ["uvicorn", "ecl_scoring_service:app", "--host", "0.0.0.0", "--port", "8003"]
