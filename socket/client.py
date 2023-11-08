import socket



def connection(host,port,i = 0 ):
    if i<4:
        try:
            client_socket = socket.socket()
            client_socket.connect((host, port))

        except ConnectionError:
            print("probleme connection serveur")
            return connection(host,port,i+1)
        else:
            client_socket.close()

    else:
        raise ConnectionRefusedError("connection ferme")


if __name__ == "__main__":
        try:
            host = "127.0.0.1"
            port = 11112
            connection(host,port)
        except ConnectionRefusedError as err:
            print(err)
        else:
            client_socket = socket.socket()
            client_socket.connect((host, port))
            while True:
                message = input("quel message envoyer")
                client_socket.send(message.encode())
