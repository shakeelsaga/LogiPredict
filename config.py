import os
from dotenv import load_dotenv

# I'm finding the absolute path to the folder this file is in.
basedir = os.path.abspath(os.path.dirname(__file__))

# Then, I'm loading the .env file.
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration."""
    # I need this for Flask to sign cookies and handle security.
    # I'm pulling it from the .env file, but I have a fallback just in case.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-key'
    
    # This tells SQLAlchemy where to find my database.
    # I've set up a fallback here: If I haven't set up PostgreSQL yet,
    # it will gracefully fall back to a local SQLite database file.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'logipredict.db')
    
    # I'm turning off a SQLAlchemy feature that uses unnecessary memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In a production environment, I would force the DATABASE_URL to exist
    # and remove the SQLite fallback for safety.