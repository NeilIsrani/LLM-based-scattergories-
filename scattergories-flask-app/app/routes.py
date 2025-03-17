from flask import Blueprint, render_template, request, jsonify
from app.models import Game, db
from app.ai_connect import AIValidator

bp = Blueprint('main', __name__)
validator = AIValidator()

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