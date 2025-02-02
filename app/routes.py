from flask import Blueprint, render_template, request, jsonify, current_app
from app.ai_validator import AIValidator
import random
import string
import json

bp = Blueprint('main', __name__)
validator = AIValidator()

@bp.route('/')
def index():
    """Serve the main game page"""
    try:
        return render_template('game.html')
    except Exception as e:
        return jsonify({'error': 'Failed to load game page', 'details': str(e)}), 500

""" @bp.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.total_score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users) """

@bp.route('/api/validate', methods=['POST'])
def validate():
    """Validate a single answer"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['category', 'answer', 'letter']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        result = validator.validate_answer(
            data['category'],
            data['answer'],
            data['letter']
        )
        
        # Ensure result is JSON-serializable
        if isinstance(result, str):
            result = json.loads(result)
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 500

@bp.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new single player game"""
    try:
        random_letter = random.choice(string.ascii_uppercase)
        return jsonify({
            'status': 'success',
            'letter': random_letter,
            'categories': [
                'Countries',
                'Animals',
                'Foods',
                'Names',
                'Things',
                'Sports'
            ]
        })
    except Exception as e:
        return jsonify({'error': 'Failed to start new game', 'details': str(e)}), 500

@bp.route('/api/submit-round', methods=['POST'])
def submit_round():
    """Submit and validate all answers for a round"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        letter = data.get('letter')
        answers = data.get('answers', {})
        
        if not letter or not answers:
            return jsonify({'error': 'Missing letter or answers'}), 400

        results = {}
        total_score = 0
        
        for category, answer in answers.items():
            validation = validator.validate_answer(
                category=category,
                answer=answer,
                letter=letter
            )
            # Ensure validation result is JSON-serializable
            if isinstance(validation, str):
                validation = json.loads(validation)
                
            results[category] = validation
            if validation.get('valid', False):
                total_score += 1

        return jsonify({
            'status': 'success',
            'results': results,
            'score': total_score,
            'letter': letter
        })
    except Exception as e:
        return jsonify({'error': 'Failed to submit round', 'details': str(e)}), 500

@bp.route('/api/status', methods=['GET'])
def game_status():
    """Check if server is running"""
    try:
        return jsonify({
            'status': 'online',
            'mode': 'single-player',
            'version': '1.0'
        })
    except Exception as e:
        return jsonify({'error': 'Status check failed', 'details': str(e)}), 500 