port = 11111
client_socket = socket.socket()
client_socket.connect((host, port))

while not flag:
        message = input("quel message envoyer")
        client_socket.send(message.encode())
        reply =client_socket.recv(1024).decode()
        print(reply)
        if  reply == "stop":
                flag = True

client_socket.close()
