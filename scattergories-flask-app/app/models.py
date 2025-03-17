from flask_sqlalchemy import SQLAlchemy
import random
import string
from app.ai_connect import AIValidator

db = SQLAlchemy()
validator = AIValidator() 

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_round = db.Column(db.Integer, default=0)
    die_roll = db.Column(db.Integer)
    prompts = db.Column(db.PickleType)
    host_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    join_code = db.Column(db.String(4), unique=True)
    letter = db.Column(db.String(1))  # Add this column

    players = db.relationship('Player', backref='game', lazy=True)

    def add_player(self, player):
        self.players.append(player)

    def roll_die(self):
        self.die_roll = random.randint(1, 20)
        letters = ["J","M","L","T","S","B","G","R","C","E",
                   "F","A","H","I","P","K","N","O","W","D"]
        self.letter = letters[self.die_roll - 1]
        return self.letter

    def create_game(self):
        """Create a new game with letter and prompts"""
        # Get letter using roll_die
        letter = self.roll_die()
        
        # Get prompts from AI validator
        prompts_data = validator.provide_round_prompts()
        self.prompts = prompts_data
        
        # Save to database
        db.session.add(self)
        db.session.commit()
        
        return {
            'letter': letter,
            'prompts': prompts_data
        }

    def calculate_scores(self, answers):
        """Calculate scores for all answers"""
        if not self.letter or not answers:
            return {'error': 'Missing letter or answers'}
            
        results = {}
        total_score = 0
        
        for category, answer in answers.items():
            validation = validator.validate_answer(
                category=category,
                answer=answer,
                letter=self.letter
            )
            results[category] = validation
            if validation.get('valid', False):
                total_score += 1
                
        return {
            'results': results,
            'total_score': total_score
        }

    def next_round(self):
        self.current_round += 1
        new_letter = self.roll_die()
        new_prompts = validator.provide_round_prompts()
        self.prompts = new_prompts
        db.session.commit()
        
        return {
            'round': self.current_round,
            'letter': new_letter,
            'prompts': new_prompts
        }

class Lobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    join_code = db.Column(db.String(4), unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref='lobby')

    def generate_join_code(self):
        self.join_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))