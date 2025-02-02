from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, default=0)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_round = db.Column(db.Integer, default=0)
    die_roll = db.Column(db.Integer)
    prompts = db.Column(db.PickleType)  # Store prompts as a list

    players = db.relationship('Player', backref='game', lazy=True)

    def add_player(self, player):
        self.players.append(player)

    def roll_die(self):
        import random
        self.die_roll = random.randint(1, 20)
        letters = ["J","M","L","T","S","B","G","R","C","E",
                   "F","A","H","I","P","K","N","O","W","D",]
        return letters[self.die_roll - 1]

    def set_prompts(self, prompts):
        self.prompts = prompts

    def calculate_scores(self):
        # Logic to calculate scores based on answers and prompts
        pass

    def next_round(self):
        self.current_round += 1
        # Logic to prepare for the next round
        pass