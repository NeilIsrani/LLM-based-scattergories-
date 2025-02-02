import random
from app import socketio
from app.models import Game, GameRound, User
from app.ai_validator import AIValidator

class ScattergoriesGame:
    CATEGORIES = [
        "Countries", "Cities", "Animals", "Foods", "Sports",
        "Celebrities", "Movies", "Books", "Occupations", "Vehicles"
    ]
    
    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ROUND_TIME = 60  # seconds

    def __init__(self):
        self.ai_validator = AIValidator()
        self.active_games = {}

    def create_game(self):
        letter = random.choice(self.LETTERS)
        categories = random.sample(self.CATEGORIES, 5)
        game = Game(letter=letter)
        return game, categories

    def validate_answer(self, category, answer, letter):
        return self.ai_validator.validate_answer(category, answer, letter)

game_manager = ScattergoriesGame() 