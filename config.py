import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Essential configs
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Basic Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # Only needed if using sessions
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # Comment out database configs for now
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///scattergories.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False