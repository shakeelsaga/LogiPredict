# LogiPredict

LogiPredict is a full-stack, production-grade web application and RESTful API that predicts shipment transit times using a trained Random Forest Regressor machine learning pipeline.

This repository hosts the stateless web/API compute layer, optimized using a multi-stage Debian-slim build, running an unprivileged system user, and utilizing Gunicorn with master process preloading for high-concurrency safety. The image is published for both `linux/amd64` and `linux/arm64` under a single multi-arch tag, so a plain `docker pull` resolves to the correct architecture automatically. It is also published in parallel to the [GitHub Container Registry](https://github.com/shakeelsaga/LogiPredict/pkgs/container/logipredict).

## Architectural Requirements

This image contains the application runtime and the pre-trained machine learning model (`model.pkl`). It can run entirely standalone: without a `DATABASE_URL`, it falls back automatically to an in-container SQLite database, which is enough to try the prediction endpoint immediately.

For persistent audit history across restarts, redeploys, or multiple replicas, connect the container to a real PostgreSQL instance by providing a valid `DATABASE_URL`. Without one, every audit log resets whenever the container restarts.

## Configuration Parameters

The container reads configuration parameters via environment runtime injection. None are strictly required to boot; the ones below control what happens when you provide them.

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `SECRET_KEY` | Symmetric encryption key for securing Flask session states. Falls back to an insecure development key if unset. | `your_secure_string` |
| `DATABASE_URL` | Fully qualified connection URI pointing to a target PostgreSQL service. If unset, falls back to SQLite. | `postgresql://user:pass@hostname:5432/dbname` |
| `FLASK_CONFIG` | Set to `production` to enforce that `DATABASE_URL` is present at startup; the container refuses to boot rather than silently falling back to SQLite. Any other value, or leaving it unset, allows the SQLite fallback. | `production` |
| `PORT` | The port Gunicorn binds to inside the container. Defaults to `5000` if unset. | `8080` |

## Quick Start: Instant Preview

To try the application immediately, with no database and no configuration:

```bash
docker run -d -p 8080:5000 shakeelsaga/logipredict:latest
```

Visit `http://localhost:8080`. This uses the SQLite fallback described above, so audit history won't persist past the container's lifetime.

## Quick Start via Docker Compose

For the full, persistent setup, orchestrate this image alongside a PostgreSQL container. This architecture handles network isolation, database health checks, and data volume mapping automatically.

Create a `docker-compose.yml` file in your workspace:

```yaml
services:
  web:
    image: shakeelsaga/logipredict:latest
    ports:
      - "${PORT:-8080}:${PORT:-8080}"
    environment:
      - SECRET_KEY=super_secure_flask_key
      - DATABASE_URL=postgresql://logi_user:logi_pass@db:5432/logipredict_db
      - PORT=${PORT:-8080}
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=logi_user
      - POSTGRES_PASSWORD=logi_pass
      - POSTGRES_DB=logipredict_db
    volumes:
      - pg_data:/var/lib/postgresql/data
    expose:
      - "5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U logi_user -d logipredict_db"]
      interval: 5s
      timeout: 5s
      retries: 5
volumes:
  pg_data:
```

Replace the inline `SECRET_KEY` and database credentials above with your own values, or move them into a `.env` file and reference it with `env_file` instead. Hardcoding real secrets into a committed compose file is fine for a quick local test, not for anything you intend to keep around.

## Running the Stack

Launch the decoupled environment directly from your shell:

```bash
docker compose up -d
```

The application interface will be accessible on the host machine at `http://localhost:8080`, or whatever value you set for `PORT`.

## Image Tags

| Tag | Meaning |
| :--- | :--- |
| `latest` | The most recent successful build of the `main` branch. |
| `<git-sha>` | The exact commit that produced this image. Immutable, for reproducible deployments. |
| `vX.Y.Z` | A deliberate, named release milestone. Immutable once published. |

## Image Features & Optimizations

* **Multi-Stage Footprint**: Stripped of heavy OS compilation suites (`gcc`, `build-essential`) and caching modules, dropping artifact overhead significantly.
* **Principle of Least Privilege**: Drops root terminal inheritance at build time; processes are executed by a restricted, non-root application user (`logiuser`).
* **PID 1 Signal Handling**: Uses Gunicorn as the explicit process manager to route kernel termination events gracefully (`SIGTERM`).
* **Race Condition Mitigation**: Built with worker pool memory preloading (`--preload`) to safeguard system catalogs during multi-worker initialization steps.
* **Multi-Architecture Builds**: Published for `linux/amd64` and `linux/arm64` from a single tag, built via Docker Buildx and QEMU.