

import socket
import threading

boucle = False
port = 11111
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(3)
clients = []  # List to store connected client sockets
clients_lock = threading.Lock()

def reception(conn):
    global boucle

    try:
        while not boucle:
            print("Listening for messages from client:", conn)
            message = conn.recv(1024).decode()
            print(f"Received message from client {conn}: {message}")

            if message == "stop":
                reply = "stop"
                conn.send(reply.encode())
                break  # Break the loop to close the current client connection

            elif message == "arret":
                reply = "stop"
                with clients_lock:
                    for client_socket in clients:
                        if client_socket != conn:  # Check if the client is still in the list
                            client_socket.send(reply.encode())
                boucle = True  # Set loop flag to terminate the main loop

            else:
                reply = f"Message received: {message}"
                print(reply)
                with clients_lock:
                    for client_socket in clients:
                        if client_socket != conn:  # Check if the client is still in the list
                            client_socket.send(reply.encode())

    except ConnectionResetError:
        print(f"Client {conn} disconnected")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

def connection():
    global boucle, clients

    try:
        while not boucle:
            conn, address = server_socket.accept()
            print(f"New client connected: {address}")
            with clients_lock:
                clients.append(conn)  # Add new client socket to the list
            retour = threading.Thread(target=reception, args=[conn])
            retour.start()

            # Remove disconnected clients
            with clients_lock:
                clients = [client_socket for client_socket in clients if client_socket.fileno() != -1]

    except ConnectionAbortedError:
        print("Server shutdown")
    except KeyboardInterrupt:
        print("Server shutdown")
    except OSError:
        print("No client")
    finally:
        server_socket.close()

if __name__ == "__main__":
    connection()
