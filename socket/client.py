import socket



def connection(host,port,i = 0 ):
    if i>10:
        try:
            client_socket = socket.socket()
            client_socket.connect((host, port))

        except ConnectionError:
            print("probleme connection serveur")
            return connection(host,port,i+1)

    else:
        raise ConnectionRefusedError("connection ferme")


if __name__ == "__main__":
    try:
        host = "10.128.2.13"
        port = 10000
        connection(host,port)
    except ConnectionRefusedError:
        print("fin la connection")
    else:
        client_socket = socket.socket()
        message = input("quel message envoyer")
        client_socket.send(message.encode())
