# LogiPredict

LogiPredict is a full-stack web application and RESTful API designed to predict shipment transit times based on historical routing data. The architecture couples an immutable Machine Learning prediction engine with a decoupled Flask backend and a brutalist custom frontend interface.

## Primary Features

* **Predictive Engine:** Utilizes a trained Random Forest Regressor pipeline to estimate delivery windows.
* **Production-Grade Server Architecture:** Built on multi-stage Docker builds, utilizing a restricted, non-root user account and Gunicorn master process preloading for safe, concurrent request handling.
* **Persistent Auditing:** Enforces full logging of every transit query to a transaction-safe database backing layer using SQLAlchemy.
* **Decoupled Configuration:** Follows cloud-native best practices (12-Factor App) by injecting structural configs and credentials dynamically at runtime via environment variables.

---

## 1. Quick Start (Containerized Deployment)

The recommended workflow to launch LogiPredict is via multi-container orchestration. This provisions an isolated virtual bridge network, spins up a PostgreSQL backend, hooks up persistent data tracking, and handles boot synchronization automatically.

### Prerequisites
* Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) or the Docker Engine daemon is installed and running.

### Execution Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shakeelsaga/LogiPredict.git](https://github.com/shakeelsaga/LogiPredict.git)
   cd LogiPredict
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory to define runtime configurations. Keep this file excluded from version control:

   ```env
   SECRET_KEY=your_secure_session_encryption_key
   DATABASE_URL=postgresql://logi_user:logi_pass@db:5432/logipredict_db
   ```

3. **Orchestrate and Boot the Stack:**
   ```bash
   docker compose up --build
   ```
   The orchestration layer will verify database health and initialize the web workers. The interface will immediately become available on the host machine at `http://localhost:8080`.

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
   Ensure a `.env` configuration file exists in your workspace root. Leaving the `DATABASE_URL` line entirely blank forces the engine to automatically build and fallback onto a local SQLite database file instance inside the development scope:
   ```bash
   python run.py
   ```
   The development server will mount locally on `http://127.0.0.1:5000`.

---

## Technical Stack Architecture

* **Backend & API Logic:** Python, Flask, Flask-SQLAlchemy, Flask-Marshmallow
* **Machine Learning & Pipeline Vectors:** Scikit-Learn, Pandas, Joblib
* **Frontend UI Layout:** Brutalist CSS, HTML5, Vanilla JavaScript, Fetch API (Zero External Framework Dependencies)
* **Production Application Process Server:** Gunicorn WSGI
* **Database Backing Engines:** PostgreSQL (Production Container Network Layer) / SQLite (Local Native Fallback Mode)

---

## License

Distributed under the MIT License. See `LICENSE` for details.