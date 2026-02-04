# I'm creating a Flask app to serve my logistics analysis and prediction models.
# This is the main file for my backend API.

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import logistics_analysis

app = Flask(__name__)

# I'm loading my trained machine learning model here.
# I need to make sure the model is trained and saved before I run this.
try:
    model = joblib.load('model.pkl')
    print("AI Model Loaded Successfully.")
except:
    print("WARNING: 'model.pkl' not found. I should run model_train.py first.")
    model = None

@app.route('/')
def home():
    # This is just a simple route to check if the API is running.
    return "LogiPredict API is Running. I can use /analyze or /predict endpoints."

@app.route('/analyze', methods=['POST'])
def analyze_data():
    # This endpoint is for analyzing the raw JSON data I get.
    # It's like a mini-ETL pipeline.
    try:
        data = request.json
        if not data:
            return jsonify({"error": "I need to provide some data"}), 400
            
        # Here, I'm using the logic from my logistics_analysis.py file.
        results = logistics_analysis.process_shipment_data(data)
        
        # I'm using Pandas to calculate some summary statistics.
        df = pd.DataFrame(results)
        summary = {
            "total_shipments": len(df),
            "avg_transit_time": round(df['transit_hours'].mean(), 2),
            "fastest_delivery": df['transit_hours'].min(),
            "slowest_delivery": df['transit_hours'].max()
        }
        
        # I'm returning the summary and a few rows of the detailed data.
        return jsonify({
            "summary": summary,
            "details": results[:5]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_delivery():
    # This endpoint is for predicting the transit time for a new shipment.
    # I need to provide the origin, destination, weight, and service type.
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        req = request.json
        
        # I'm creating a DataFrame here to match the input format my model expects.
        input_data = pd.DataFrame([{
            'origin_city': req.get('origin', '').upper(),
            'destination_city': req.get('destination', '').upper(),
            'weight_kg': float(req.get('weight', 1.0)),
            'service_type': req.get('service', 'FEDEX_EXPRESS_SAVER')
        }])

        prediction = model.predict(input_data)[0]
        
        # I'm returning the predicted transit time and the route.
        return jsonify({
            "estimated_transit_hours": round(prediction, 2),
            "route": f"{req.get('origin')} -> {req.get('destination')}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # I'm running the Flask app here.
    app.run(debug=True, port=5000)