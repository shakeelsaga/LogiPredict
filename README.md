# LogiPredict: My Smart Logistics Analyzer

This project is my attempt to build a smart system that can take messy logistics data, make sense of it, and even predict how long shipments will take. I'm using machine learning to power this, and it's been a great way to apply my skills to a real-world problem.

## What I'm Trying to Do

I wanted to see if I could build something that would:

*   **Tidy up messy data:** Logistics data can be a real headache, with lots of nested JSON and inconsistent formats. I've written scripts to clean and organize it automatically.
*   **Find useful insights:** I'm calculating key metrics like average transit time and shipment velocity to understand performance.
*   **Predict the future:** The core of this project is a machine learning model that can predict shipment transit times based on factors like origin, destination, and weight.

## How I Built It

I used a few key technologies to put this all together:

*   **Python:** The whole project is built in Python.
*   **Flask:** I used Flask to create a simple API that I can use to interact with my analytics and prediction models.
*   **Pandas:** Pandas is my go-to for data manipulation. It's been essential for cleaning and preparing the data for my model.
*   **Scikit-Learn:** This is what I'm using for the machine learning side of things. I've trained a Random Forest Regressor to make the predictions.
*   **Joblib:** I'm using Joblib to save my trained model so I can easily use it in my application.

## How to Get It Running

Here are the steps to get this project up and running on your own machine:

1.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Train the model:**
    ```bash
    python model_train.py
    ```
3.  **Run the server:**
    ```bash
    python app.py
    ```

## How to Use the API

I've set up a couple of API endpoints to interact with my system:

*   `POST /analyze`: Send a POST request with your raw JSON data to this endpoint, and it will return a summary of the performance metrics.
*   `POST /predict`: Send a POST request with the shipment details (origin, destination, and weight), and it will return a prediction for the delivery time.
