from flask import Flask
from config import Config
from flask_cors import CORS  # If you're using CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS if needed
    CORS(app)
    
    # Remove login manager
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    
    # Remove socket initialization
    # socketio = SocketIO()
    # socketio.init_app(app)
    
    # Remove session handling
    # Session(app)
    
    # Register routes blueprint
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app 