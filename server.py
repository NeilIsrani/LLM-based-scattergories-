import socket
import threading

# Server setup
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 5001      # Port for the chat room

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    """Send message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client):
    """Handle communication from a single client."""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames.pop(index)
            broadcast(f"{nickname} has left the chat.".encode('utf-8'))
            break

def receive_connections():
    """Accept new connections and start a new thread for each client."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"New connection from {address}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of new client: {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the chat room!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
