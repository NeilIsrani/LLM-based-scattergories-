import random
import time
import string
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import db, Player, Game, Lobby

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
    return render_template('game.html')

@main.route('/create_lobby', methods=['POST'])
def create_lobby():
    data = request.json
    player = Player(name=data['name'])
    game = Game()
    lobby = Lobby(game=game)
    lobby.generate_join_code()
    game.host_id = player.id
    db.session.add(player)
    db.session.add(game)
    db.session.add(lobby)
    db.session.commit()
    return jsonify({'join_code': lobby.join_code, 'host_id': player.id}), 201

@main.route('/join_lobby', methods=['POST'])
def join_lobby():
    data = request.json
    lobby = Lobby.query.filter_by(join_code=data['join_code']).first()
    if not lobby:
        return jsonify({'message': 'Lobby not found'}), 404
    player = Player(name=data['name'], game_id=lobby.game.id)
    db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Player joined successfully'}), 200

@main.route('/start_game_api', methods=['POST'])
def start_game_api():
    data = request.json
    game = Game.query.get(data['game_id'])
    if game.host_id != data['host_id']:
        return jsonify({'message': 'Only the host can start the game'}), 403
    # Logic to start the game
    return jsonify({'message': 'Game started successfully'}), 200

@main.route('/remove_player', methods=['POST'])
def remove_player():
    data = request.json
    game = Game.query.get(data['game_id'])
    if game.host_id != data['host_id']:
        return jsonify({'message': 'Only the host can remove players'}), 403
    player = Player.query.get(data['player_id'])
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player removed successfully'}), 200

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