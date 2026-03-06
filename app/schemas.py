from flask_marshmallow import Marshmallow
from app.models import PredictionLog

# I'm initializing Marshmallow here, and I'll bind it to the app soon.
ma = Marshmallow()

class PredictionLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # I'm telling Marshmallow to look at my PredictionLog database table
        # and figure out how to convert it to JSON automatically.
        model = PredictionLog
        load_instance = True

# I'm creating an instance of the schema to use in my routes.
prediction_schema = PredictionLogSchema()