![Version](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshakeelsaga%2FLogiPredict%2Fmain%2FVERSION&search=(.*)&label=version&color=blue)
# LogiPredict

LogiPredict is a full-stack web application and RESTful API designed to predict shipment transit times based on historical routing data. The architecture couples an immutable Machine Learning prediction engine with a decoupled Flask backend and a brutalist custom frontend interface.

**Current release:** `v1.1.4`

## Primary Features

* **Predictive Engine:** Utilizes a trained Random Forest Regressor pipeline to estimate delivery windows.
* **Production-Grade Server Architecture:** Built on multi-stage Docker builds, utilizing a restricted, non-root user account and Gunicorn master process preloading for safe, concurrent request handling.
* **Persistent Auditing:** Enforces full logging of every transit query to a transaction-safe database backing layer using SQLAlchemy.
* **Decoupled Configuration:** Follows cloud-native best practices (12-Factor App) by injecting structural configs and credentials dynamically at runtime via environment variables.
* **Multi-Architecture Distribution:** Published as a single multi-arch image (`linux/amd64` + `linux/arm64`) to both Docker Hub and the GitHub Container Registry, built automatically on every push to `main`.

---

## 1. Quick Start

There are two ways to run LogiPredict, depending on what you're after.

### 1.1 Instant Preview (no clone required)

Pull and run the published image directly, with no repository, no configuration, and no database setup required:

```bash
docker run -d -p 8080:5000 shakeelsaga/logipredict:latest
```

or, identically, from the GitHub Container Registry:

```bash
docker run -d -p 8080:5000 ghcr.io/shakeelsaga/logipredict:latest
```

Visit `http://localhost:8080`. This mode uses an in-container SQLite fallback for the audit log, which is fine for a quick look, but the data doesn't persist past the container's lifetime. For the full architecture described above, use 1.2.

### 1.2 Full Local Deployment (Docker Compose)

This is the recommended path: an isolated bridge network, a persistent PostgreSQL backend, and automatic boot synchronization.

#### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) or the Docker Engine daemon, installed and running.

#### Execution Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shakeelsaga/LogiPredict.git](https://github.com/shakeelsaga/LogiPredict.git)
   cd LogiPredict
   ```

2. **Configure environment variables:**
   Copy the provided template and fill it in, and keep the resulting `.env` excluded from version control:

   ```bash
   cp .env.example .env
   ```

   ```env
   SECRET_KEY=
   DATABASE_URL=postgresql://logi_user:logi_pass@db:5432/logipredict_db
   PORT=8080
   POSTGRES_USER=logi_user
   POSTGRES_PASSWORD=logi_pass
   POSTGRES_DB=logipredict_db
   ```

   Generate a real `SECRET_KEY` rather than leaving it blank:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   If you change `POSTGRES_USER`, `POSTGRES_PASSWORD`, or `POSTGRES_DB` from their defaults, update the credentials embedded in `DATABASE_URL` to match, since the two are read independently and won't stay in sync automatically.

3. **Deploy:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
   This pulls the current published multi-arch image when your platform is supported (`amd64` or `arm64`), and falls back to building from source only if it isn't. The interface becomes available at `http://localhost:8080`, or whatever value you set for `PORT` in `.env`.

   To force a rebuild from source instead of pulling, for example while testing a local code change before you push, run `docker compose up --build` directly instead of `deploy.sh`.

---

## 2. Using the REST API

The application exposes a structured JSON-first API endpoint for embedding logistics calculations into upstream workflows.

### `POST /api/predict`

Calculates estimated transit windows and persists parameters to the audit log.

**Headers:** `Content-Type: application/json`

**Request Format (JSON):**
```json
{
  "origin": "DELHI",
  "destination": "CHENNAI",
  "weight": 12.5,
  "service": "STANDARD_OVERNIGHT"
}
```

**Success Response (200 OK):**
```json
{
  "id": 12,
  "origin_city": "DELHI",
  "destination_city": "CHENNAI",
  "weight_kg": 12.5,
  "service_type": "STANDARD_OVERNIGHT",
  "predicted_hours": 24.32,
  "created_at": "2026-06-01T12:00:00Z"
}
```

---

## 3. Development & Model Training (Native Local Setup)

Follow this approach if you are a contributor who needs to train the core machine learning models or modify application logic natively without a container daemon.

### Prerequisites
* Python 3.11+ installed.
* Access to C compilers (`gcc`/`build-essential`) to build pre-compiled mathematical wheels for numerical computation libraries.

### Execution Steps

1. **Initialize a local virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install project requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Predictive Model:**
   To parse raw tracking logs (`dummy_dataset.json`) and serialize a new preprocessing pipeline binary (`model.pkl`), run:
   ```bash
   python model_train.py
   ```

4. **Boot Development Web Server:**
   Ensure a `.env` configuration file exists in your workspace root. Leaving the `DATABASE_URL` line entirely blank forces the engine to automatically build and fall back onto a local SQLite database file instance inside the development scope:
   ```bash
   python run.py
   ```
   The development server will mount locally on `http://127.0.0.1:5000`.

---

## 4. Deployment & CI/CD Pipeline

Every push to `main` that touches application code, dependencies, or infrastructure (but not documentation or metadata files) triggers a GitHub Actions workflow that does the following.

1. Builds a single multi-architecture image (`linux/amd64` and `linux/arm64`) using Docker Buildx and QEMU.
2. Publishes it to both [Docker Hub](https://hub.docker.com/r/shakeelsaga/logipredict) and the [GitHub Container Registry](https://github.com/shakeelsaga/LogiPredict/pkgs/container/logipredict) in the same run.
3. Tags it three ways on each registry, described below.

The workflow can also be triggered manually from the repository's Actions tab, without requiring a code change.

### Versioning & Image Tags

| Tag | Meaning | Stability |
|---|---|---|
| `latest` | The most recent successful build of `main`. | Moves with every qualifying push. |
| `<git-sha>` | The exact commit that produced this image. | Immutable. Use this for reproducible deployments or rollback. |
| `v1.1.1` (from the `VERSION` file) | A deliberate release milestone, bumped by hand when a change is significant enough to name. | Immutable once published; changes only when `VERSION` is edited. |

Both registries carry identical tags and identical multi-arch manifests, so pulling from either gives you the same image.

---

## Technical Stack Architecture

* **Backend & API Logic:** Python, Flask, Flask-SQLAlchemy, Flask-Marshmallow
* **Machine Learning & Pipeline Vectors:** Scikit-Learn, Pandas, Joblib
* **Frontend UI Layout:** Brutalist CSS, HTML5, Vanilla JavaScript, Fetch API (Zero External Framework Dependencies)
* **Production Application Process Server:** Gunicorn WSGI
* **Database Backing Engines:** PostgreSQL (Production Container Network Layer) / SQLite (Local Native Fallback Mode)
* **CI/CD & Distribution:** GitHub Actions, Docker Buildx (multi-arch), Docker Hub, GitHub Container Registry

---

## License

Distributed under the MIT License. See `LICENSE` for details.