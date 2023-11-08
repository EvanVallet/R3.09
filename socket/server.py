import socket


port = 11112
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)
while True:
    try:
        message = conn.recv(1024).decode()
    except:
        conn, address = server_socket.accept()
    else:
        print(message)
        if message == "bye":
            conn.close()
        elif message == "arret":
             break

server_socket.close()
