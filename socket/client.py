import socket

host = "10.128.2.13"
port = 10000

def connection(host,port,i = 0 ):
    if i>10:
        try:
            client_socket = socket.socket()
            client_socket.connect((host, port))
        except ConnectionError:
            print("probleme connection serveur")
            return connection(host,port,i+1)
        else:
            message=input("quel message envoyer")
            client_socket.send(message.encode())
            return
    else:
        client_socke
        raise ConnectionRefusedError("connection ferme")
        
        
