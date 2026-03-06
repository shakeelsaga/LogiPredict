# LogiPredict

LogiPredict is a full-stack web application that predicts shipment transit times based on historical routing data. It combines a Machine Learning prediction engine with a RESTful backend and a custom frontend interface.

## Overview

*   **Predictive Engine:** Uses a trained Random Forest Regressor to estimate delivery windows.
*   **API-First Architecture:** The backend serves JSON data, decoupling the logic from the UI.
*   **Persistent Auditing:** Logs every estimation request to a database using SQLAlchemy.
*   **Environment Agnostic:** Falls back to a local SQLite database if a cloud PostgreSQL URL is not provided.
*   **Custom UI:** A zero-dependency frontend built with Vanilla JS, CSS, and the Fetch API.

## Tech Stack

*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Marshmallow
*   **Machine Learning:** Scikit-Learn, Pandas, Joblib
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript
*   **Server:** Gunicorn

## Running the Application Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shakeelsaga/LogiPredict.git
    cd LogiPredict
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    *On Windows, use `venv\Scripts\activate`*

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment variables:**
    Create a `.env` file in the root directory and add a secret key:
    ```
    SECRET_KEY=your_generated_secret_key_here
    ```
    *Leave `DATABASE_URL` blank to default to local SQLite.*

5.  **Run the server:**
    ```bash
    python run.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Using the API

The backend exposes a RESTful endpoint for transit time calculation.

### POST /api/predict

Calculates the estimated transit time and logs the request to the database.

**Request Body (JSON):**
```json
{
  "origin": "DELHI",
  "destination": "CHENNAI",
  "weight": 5.3,
  "service": "FEDEX_EXPRESS_SAVER"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "created_at": "2026-03-06T15:10:31.440476",
  "origin_city": "DELHI",
  "destination_city": "CHENNAI",
  "weight_kg": 5.3,
  "service_type": "FEDEX_EXPRESS_SAVER",
  "predicted_hours": 12.88
}
```

## License

This project is licensed under the MIT License.
