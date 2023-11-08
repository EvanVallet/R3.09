import socket

host = "127.0.0.1"
port = 11112
client_socket = socket.socket()
client_socket.connect((host, port))
while True:
        message = input("quel message envoyer")
        client_socket.send(message.encode())
