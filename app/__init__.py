from flask import Flask
from config import Config
from app.models import db
from app.schemas import ma
from app.views import views_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # I'm initializing Marshmallow with the app here.
    ma.init_app(app)

    with app.app_context():
        # I'm importing the blueprints here.
        from app.api import api_bp
        from app.views import views_bp
        
        # By adding this url_prefix, I'm making every route in api.py automatically start with /api.
        # For example, /predict will become /api/predict.
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(views_bp)

        db.create_all()

    return app