from flask import Blueprint, render_template

# I'm creating a blueprint for my frontend views.
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    # I'm using render_template here, which I know looks inside the app/templates/ folder.
    return render_template('index.html')