import socket
import threading
import random
import string

# Server settings
HOST = '0.0.0.0' 
PORT = 5001

# Dictionary to store game lobbies
lobbies = {}
lock = threading.Lock()

def generate_game_code():
    """Generate a random 6-character game code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    conn.send("Welcome to the game server!\nCommands: CREATE, JOIN <CODE>\n".encode())
    
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            command = data.split()
            if command[0] == "CREATE":
                game_code = generate_game_code()
                with lock:
                    lobbies[game_code] = []
                conn.send(f"Game created. Your game code is: {game_code}\n".encode())
            elif command[0] == "JOIN" and len(command) == 2:
                game_code = command[1]
                with lock:
                    if game_code in lobbies:
                        lobbies[game_code].append(conn)
                        conn.send(f"Joined game {game_code}\n".encode())
                    else:
                        conn.send("Invalid game code.\n".encode())
            else:
                conn.send("Invalid command. Use CREATE or JOIN <CODE>.\n".encode())
        except:
            break

    conn.close()
    print(f"Connection closed: {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

