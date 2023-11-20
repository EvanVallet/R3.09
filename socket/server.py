import socket
import threading

boucle = False
port = 11111
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)



def reception():
    flag = False
    global conn , server_socket, boucle
    while not flag:
        print(1)
        try:
            message = conn.recv(1024).decode()
        except :
            conn, address = server_socket.accept()

        else:
            print(message)
            if message == "bye":
                reply="stop"
                conn.send(reply.encode())
                conn.close()
            elif message == "arret":
                 reply = "stop"
                 conn.send(reply.encode())
                 flag = True
                 server_socket.close()
                 boucle=True
            else :
                reply="message pris en compte sont :\n         bye = deconexion \n         arret = arret"
                conn.send(reply.encode())
    server_socket.close()

retour = threading.Thread(target=reception)

start= False
try:
    conn, address = server_socket.accept()
    while not boucle:
        if start == False :
            print("start")
            retour.start()
            start = True
        message=str(input("message a envoyer"))
        conn.send(message.encode())
except ConnectionAbortedError:
    print("arret du server")

except KeyboardInterrupt:
    print("arret du server")

except OSError:
    print("pas de client")


server_socket.close()
