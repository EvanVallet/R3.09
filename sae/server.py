import socket
import threading
import mysql.connector
from mysql.connector import Error

boucle = False
port = 11111
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(3)
clients = []  # List to store connected client sockets
clients_lock = threading.Lock()

# Connect to the MySQL database
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="server",
        password="Toto123@",
        database="sae1"
    )

    if db_connection.is_connected():
        print("Connected to MySQL database")
except Error as e:
    print("Error connecting to MySQL database:", e)


def authenticate(username, password):
    # Check the credentials against the database
    cursor = db_connection.cursor()

    try:
        query = "SELECT * FROM Users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            return "success"
        else:
            return "failure"

    except Error as e:
        print("Error authenticating user:", e)
        return "failure"
    finally:
        cursor.close()


def register(username, password):
    # Register a new user in the database
    cursor = db_connection.cursor()

    try:
        # Check if the username already exists
        query = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            return "failure"  # Username already exists
        else:
            # Add the new user to the database
            query = "INSERT INTO Users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            db_connection.commit()
            return "success"

    except Error as e:
        print("Error registering user:", e)
        db_connection.rollback()
        return "failure"
    finally:
        cursor.close()


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

            elif message.startswith("login"):
                # Process login request
                username, password = message.split(" ", 2)[1:]
                reply = authenticate(username, password)
                conn.send(reply.encode())

            elif message.startswith("register"):
                # Process register request
                username, password = message.split(" ", 2)[1:]
                reply = register(username, password)
                conn.send(reply.encode())

            else:
                # Send the message to all connected clients and store it in the database
                with clients_lock:
                    for client_socket in clients:
                        if client_socket != conn:  # Check if the client is still in the list
                            client_socket.send(message.encode())

                # Store the message in the database
                store_message(username, message)

    except ConnectionResetError:
        print(f"Client {conn} disconnected")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()


def store_message(username, message):
    # Store the message in the database
    cursor = db_connection.cursor()

    try:
        query = "INSERT INTO Messages (user_id, message_text) VALUES ((SELECT user_id FROM Users WHERE username = %s), %s)"
        cursor.execute(query, (username, message))
        db_connection.commit()

    except Error as e:
        print("Error storing message:", e)
        db_connection.rollback()

    finally:
        cursor.close()


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
        db_connection.close()


if __name__ == "__main__":
    connection()
