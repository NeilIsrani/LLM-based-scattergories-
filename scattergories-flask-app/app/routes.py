import random
import time
from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__)

# List of prompts (you can replace these with your own prompts)
PROMPTS = [
    "A fruit", "A city", "A movie title", "A book title", "A famous person",
    "A color", "A country", "A sport", "A food", "An animal", "A brand", "A song title"
]

def generate_prompt():
    return random.sample(PROMPTS, 12)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/start_game', methods=['POST'])
def start_game():
    player_name = request.form.get('player_name')
    session['players'] = [player_name]
    session['scores'] = {player_name: 0}
    session['current_round'] = 1
    return redirect(url_for('main.game'))

@main.route('/game')
def game():
    if 'players' not in session:
        return redirect(url_for('main.index'))
    
    session['prompt'] = generate_prompt()
    session['start_time'] = time.time()
    return render_template('game.html', prompt=session['prompt'], players=session['players'])

@main.route('/submit_answers', methods=['POST'])
def submit_answers():
    answers = request.form.to_dict(flat=False)
    session['answers'] = answers
    return redirect(url_for('main.vote'))

@main.route('/vote')
def vote():
    if 'answers' not in session:
        return redirect(url_for('main.index'))
    
    return render_template('vote.html', answers=session['answers'], players=session['players'])

@main.route('/submit_votes', methods=['POST'])
def submit_votes():
    votes = request.form.to_dict(flat=False)
    for player, player_votes in votes.items():
        session['scores'][player] += sum(int(vote) for vote in player_votes)
    
    session['current_round'] += 1
    if session['current_round'] > 3:
        return redirect(url_for('main.results'))
    else:
        return redirect(url_for('main.game'))

@main.route('/results')
def results():
    return render_template('results.html', scores=session['scores'])