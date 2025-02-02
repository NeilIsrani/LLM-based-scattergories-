import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f09f92a98d1a8b9e8f1b8b9e8f1b8b9e8f1b8b9e8f1b8b9e'
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///scattergories.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_TYPE = 'filesystem'