import socket
import threading
import json

with open('settings.json') as f:
    _settings = json.loads(f.read())
    SERVER_HOST = str(_settings["SERVER_HOST"])
    SERVER_PORT = int(_settings["SERVER_PORT"])
    f.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("Received:", message)
        except:
            print("Connection closed")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    client_socket.send(message.encode())

client_socket.close()
