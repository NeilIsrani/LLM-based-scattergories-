from flask import Blueprint, render_template, request, jsonify
from app.models import Game, db
from app.ai_connect import AIValidator

bp = Blueprint('main', __name__)
validator = AIValidator()
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

@bp.route('/')
def index():
    """Serve the main game page"""
    return render_template('game.html')

@bp.route('/api/new-game', methods=['POST'])
def new_game():
    """Create a new game using Game model"""
    try:
        # Create new game instance
        game = Game()
        
        # Call create_game method from model
        game_data = game.create_game()
        
        return jsonify({
            'status': 'success',
            'letter': game_data['letter'],
            'die_roll': game.die_roll,  # Include the actual die roll
            'prompts': game_data['prompts'],
            'game_id': game.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/submit-round', methods=['POST'])
def submit_round():
    """Submit and validate answers using Game model"""
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        answers = data.get('answers', {})
        
        # Get the game instance
        game = Game.query.get(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
            
        # Calculate scores using model method
        results = game.calculate_scores(answers)
        
        return jsonify({
            'status': 'success',
            'results': results['results'],
            'score': results['total_score'],
            'letter': game.letter
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/next-round', methods=['POST'])
def next_round():
    """Start next round using Game model"""
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        
        game = Game.query.get(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
            
        # Use model method for next round
        round_data = game.next_round()
        
        return jsonify({
            'status': 'success',
            'round': round_data['round'],
            'letter': round_data['letter'],
            'prompts': round_data['prompts']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
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