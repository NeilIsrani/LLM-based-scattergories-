import socket
import threading

SERVER_IP = "18.221.208.115"  # Get the host's IP address
PORT = 5000  # Same port as the server

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def receive_messages():
    """Receive messages from the server and print them."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Disconnected from the server.")
            client.close()
            break

def send_messages():
    """Send messages to the server."""
    while True:
        message = input("")
        client.send(f"{nickname}: {message}".encode('utf-8'))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
