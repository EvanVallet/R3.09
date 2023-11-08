import socket

host = "10.128.2.13"
port = 10000

client_socket = socket.socket()

client_socket.connect((host, port))
message=input("quel message envoyer")
client_socket.send(message.encode())

reply = client_socket.recv(1024).decode()

client_socket.close()