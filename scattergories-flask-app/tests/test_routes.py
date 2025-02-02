from app import app

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Start a New Game' in response.data

def test_roll_die(client):
    response = client.get('/roll_die')
    assert response.status_code == 200
    assert b'rolled' in response.data

def test_submit_answer(client):
    response = client.post('/submit_answer', data={'answer': 'Apple', 'category': 'Fruit'})
    assert response.status_code == 200
    assert b'Answer submitted' in response.data

def test_get_prompts(client):
    response = client.get('/get_prompts')
    assert response.status_code == 200
    assert b'Prompts' in response.data

def test_score_calculation(client):
    response = client.post('/calculate_score', data={'player_id': 1})
    assert response.status_code == 200
    assert b'Score' in response.data