import socket
import threading
import json

with open('settings.json') as f:
    _settings = json.loads(f.read())
    SERVER_HOST = str(_settings["SERVER_HOST"])
    SERVER_PORT = int(_settings["SERVER_PORT"])
    f.close()
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = []

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Received message from {client_address}: {message}")

            for client in clients:
                if client != client_socket:
                    client.send(message.encode())
        except:
            break

    print(f"Connection from {client_address} closed")
    clients.remove(client_socket)
    client_socket.close()

print("Server listening on", SERVER_HOST, ":", SERVER_PORT)

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
