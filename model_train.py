import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import logistics_analysis

# 1. I'm loading my dataset here. I'm using the dummy dataset for now.
with open("dummy_dataset.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 2. I'm processing the data using the logic from my logistics_analysis.py file.
print("Processing data...")
clean_data = logistics_analysis.process_shipment_data(raw_data)
df = pd.DataFrame(clean_data)

# 3. I'm filtering out any rows that don't have a valid transit time.
df = df[df['transit_hours'] > 0]

print(f"Training on {len(df)} shipments...")

# 4. I'm defining my features (X) and target (y) here.
# These are the inputs and outputs for my machine learning model.
X = df[['origin_city', 'destination_city', 'weight_kg', 'service_type']]
y = df['transit_hours']

# 5. I'm building a pipeline to preprocess the data and train the model.
# I'm using OneHotEncoder to convert the categorical features into a format that the model can understand.
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['origin_city', 'destination_city', 'service_type'])
    ],
    remainder='passthrough'
)

model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 6. I'm splitting the data into training and testing sets and then training the model.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model_pipeline.fit(X_train, y_train)

# I'm printing the accuracy of the model on the test set.
print(f"Model Accuracy (R2 Score): {model_pipeline.score(X_test, y_test):.2f}")

# 7. I'm saving the trained model so I can use it in my application.
joblib.dump(model_pipeline, 'model.pkl')
print("Success! Model saved as 'model.pkl'")