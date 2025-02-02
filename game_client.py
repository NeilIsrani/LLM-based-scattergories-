import socket

# Server settings
HOST = '3.143.1.16'  # Must match server's IP
PORT = 5001

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    welcome_message = client.recv(1024).decode()
    print(welcome_message)
    
    while True:
        command = input("Enter command (CREATE, JOIN <CODE>, or LEAVE): ").strip()
        if command:
            if command.upper() == "LEAVE":
                client.send(command.encode())
                print("Disconnected from server.")
                client.close()
                break
            client.send(command.encode())
            response = client.recv(1024).decode()
            print(response)

if __name__ == "__main__":
    start_client()

