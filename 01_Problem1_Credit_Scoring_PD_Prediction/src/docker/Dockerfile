# Build context is src/ itself -- this service's code lives in src/fastapi_service/
# (see docker-compose.yml's `build: context: .., dockerfile: docker/Dockerfile`, or build
# manually with:
#     docker build -f docker/Dockerfile -t amex-pd-api .
# run from 01_Problem1_Credit_Scoring_PD_Prediction/src/ itself).
#
# Fixed 2026-09-09: this Dockerfile previously did `COPY requirements-api.txt .` /
# `COPY main.py .`, which only works if those files sit directly in the build context
# root -- they actually live in src/fastapi_service/, one level down, so `docker build`
# failed with "not found" on both COPY lines. Never caught earlier because this sandbox's
# Docker CLI has no daemon/registry access (see ROADMAP.md); flagged in the 2026-08-25
# hardening pass, fixed here once GitHub's own runners (which do have real Docker access)
# made it possible to verify for real.
FROM python:3.11-slim

WORKDIR /app

COPY fastapi_service/requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY fastapi_service/main.py .

RUN useradd --create-home --uid 1000 amexapi && chown -R amexapi:amexapi /app
USER amexapi

ENV AMEX_PROJECT_ROOT=/mnt/amex-project

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
