import socket
import threading


flag = False
host = "127.0.0.1"
port = 11111
client_socket = socket.socket()


#while not flag:
#        message = input("quel message envoyer")
#        client_socket.send(message.encode())
#        reply =client_socket.recv(1024).decode()
#        print(reply)
#        if  reply == "stop":
#                flag = True
#
#client_socket.close()



def reception():
    flag = False
    global client_socket
    while not flag:
        print(1)
        reply = client_socket.recv(1024).decode()
        print(reply)
        if reply == "stop":
            client_socket.close()
            flag=True
    client_socket.close()

retour = threading.Thread(target=reception)

start= False
try:
    client_socket.connect((host, port))
    while not flag:
        if start == False :
            print("start")
            retour.start()
            start = True
        message=str(input("message a envoyer"))
        client_socket.send(message.encode())
except ConnectionAbortedError:
    print("arret de la connexion")
    flag = True
except OSError:
    print("arret de la connexion")
    flag = True

client_socket.close()
retour.join()
