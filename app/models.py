from app import db, login_manager
# from flask_login import UserMixin  # Comment out
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User():  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    total_score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    letter = db.Column(db.String(1), nullable=False)
    round_number = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    
class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(100))
    answer = db.Column(db.String(100))
    score = db.Column(db.Integer, default=0) 