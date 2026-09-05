import os
from flask import Flask
from config import Config, ProductionConfig
from app.models import db
from app.schemas import ma
from app.views import views_bp

def create_app():
    flask_config = os.environ.get('FLASK_CONFIG', 'development')

    if flask_config == 'production':
        if not os.environ.get('DATABASE_URL'):
            raise RuntimeError(
                "DATABASE_URL must be set when FLASK_CONFIG=production. "
                "Refusing to silently fall back to SQLite in production."
            )
        config_class = ProductionConfig
    else:
        config_class = Config

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