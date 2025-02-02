from app.models import Player, Game

def test_player_initialization():
    player = Player(name="Alice")
    assert player.name == "Alice"
    assert player.score == 0

def test_game_initialization():
    game = Game()
    assert len(game.players) == 0
    assert game.round == 1

def test_add_player():
    game = Game()
    player = Player(name="Bob")
    game.add_player(player)
    assert len(game.players) == 1
    assert game.players[0].name == "Bob"

def test_update_score():
    player = Player(name="Charlie")
    player.update_score(10)
    assert player.score == 10

def test_validate_answer_correct():
    game = Game()
    game.add_player(Player(name="Diana"))
    prompt = "Fruit"
    answer = "Apple"
    assert game.validate_answer(answer, prompt) == True

def test_validate_answer_incorrect():
    game = Game()
    game.add_player(Player(name="Eve"))
    prompt = "Fruit"
    answer = "Car"
    assert game.validate_answer(answer, prompt) == False