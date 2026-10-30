# Stage 1: builder
FROM python:3.13-slim-bookworm AS builder

RUN rm -f /usr/local/lib/python3.13/site-packages/pip/_vendor/bom.cdx.json

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt "msgpack>=1.2.3" "setuptools>=78.1.1" "urllib3>=2.8.0"

RUN find /opt/venv /usr/local/lib/python3.13/site-packages/pip \
    -name "bom.cdx.json" -delete

COPY src/ src/
COPY data/churn_v1.csv data/churn_v1.csv

RUN python src/train/train.py data/churn_v1.csv models/model.joblib


# Stage 2: runtime
FROM python:3.13-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN rm -f /usr/local/lib/python3.13/site-packages/pip/_vendor/bom.cdx.json

RUN useradd --create-home --uid 10001 appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/models /app/models
COPY src/ /app/src/

ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
