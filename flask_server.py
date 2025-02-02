from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to store game lobbies
lobbies = {}

def generate_game_code():
    """Generate a random 6-character game code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@socketio.on("message")
def handle_message(msg):
    command = msg.strip().split()
    
    if command[0] == "CREATE":
        game_code = generate_game_code()
        lobbies[game_code] = []
        send(f"Game created. Your game code is: {game_code}", broadcast=False)

    elif command[0] == "JOIN" and len(command) == 2:
        game_code = command[1]
        if game_code in lobbies:
            lobbies[game_code].append(request.sid)
            send(f"Joined game {game_code}", broadcast=False)
            emit("update_lobby", lobbies[game_code], room=game_code)
        else:
            send("Invalid game code.", broadcast=False)

    elif command[0] == "DISCONNECT":
        send("Disconnecting from server.", broadcast=False)

@socketio.on("join_lobby")
def join_lobby(data):
    game_code = data["gameCode"]
    if game_code in lobbies:
        join_room(game_code)
        lobbies[game_code].append(request.sid)
        emit("update_lobby", lobbies[game_code], room=game_code)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)

