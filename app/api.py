import os
import joblib
import pandas as pd
from flask import Blueprint, request, jsonify
from app.models import db, PredictionLog
from app.schemas import prediction_schema

# I'm defining the blueprint here. All these routes will be prefixed with /api.
api_bp = Blueprint('api', __name__)

# I'm safely loading my ML model using absolute paths to avoid issues in production.
basedir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(basedir, 'ml', 'model.pkl')

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    model = None
    print("WARNING: model.pkl not found in app/ml/ directory.")

@api_bp.route('/predict', methods=['POST'])
def predict_delivery():
    if not model:
        return jsonify({"error": "Model not loaded on server."}), 500

    try:
        # 1. First, I get the JSON data sent from the frontend.
        req = request.json
        
        # I extract the variables, with fallbacks to prevent crashes.
        origin = req.get('origin', '').upper()
        destination = req.get('destination', '').upper()
        weight = float(req.get('weight', 1.0))
        service = req.get('service', 'FEDEX_EXPRESS_SAVER')

        # 2. I need to format the data for the ML model, just like before.
        input_data = pd.DataFrame([{
            'origin_city': origin,
            'destination_city': destination,
            'weight_kg': weight,
            'service_type': service
        }])

        # 3. Now I can get the prediction.
        prediction = model.predict(input_data)[0]
        estimated_hours = float(round(prediction, 2))

        # 4. This is new: I'm saving the prediction to my database.
        new_log = PredictionLog(
            origin_city=origin,
            destination_city=destination,
            weight_kg=weight,
            service_type=service,
            predicted_hours=estimated_hours
        )
        db.session.add(new_log)
        db.session.commit() # This officially writes it to my logipredict.db file.

        # 5. I'll return the newly saved database record as clean JSON.
        return prediction_schema.jsonify(new_log), 200

    except Exception as e:
        # If anything crashes, I'll roll back the database to prevent corruption.
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500