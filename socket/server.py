import socket
import threading

flag = False
port = 11112
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)




def reception(server_socket):
    flag = False
    while not flag:
        try:
            message = conn.recv(1024).decode()
        except:
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
            else :
                reply="message pris en compte sont :\n         bye = deconexion \n         arret = arret"
                conn.send(reply.encode())
    server_socket.close()

retour = threading.Thread(target=reception,args=server_socket)

while not flag:
    try:
        # try:
        #     message = str(input("message a envoyer"))
        #     conn.send(message.encode())
        # except NameError:
        #     conn, address = server_socket.accept()

    except OSError:
        print("arret du server")
        flag = True



server_socket.close()
