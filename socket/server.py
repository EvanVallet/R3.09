import socket


port = 10000
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)
conn, address = server_socket.accept()
message = conn.recv(1024).decode()



if message == "bye":
    conn.close()
if message == "arret":
    server_socket.close()
