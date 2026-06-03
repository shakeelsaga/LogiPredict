# THE BUILDER

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# THE RUNNER

FROM python:3.11-slim AS runner

LABEL org.opencontainers.image.description="A containerized Machine Learning API and web interface for predicting logistics transit times."

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN addgroup --system logigroup && adduser --system --group logiuser

WORKDIR /app
RUN chown logiuser:logigroup /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=logiuser:logigroup . .

USER logiuser
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--preload", "run:app"]