#sqlalchemi
import socket
import threading
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,


)
flag = False
host = "127.0.0.1"
port = 11111
client_socket = socket.socket()


class RegisterPage(QWidget):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket  # Set the client socket

        self.setWindowTitle("Inscription")
        self.resize(400, 300)

        # Create username and password input fields
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Create a register button
        self.register_button = QPushButton("S'inscrire", self)
        self.register_button.clicked.connect(self.register)



        #Arrange elements in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Send a registration request to the server
        request = f"register {username} {password}"
        print(request)
        print(self.client_socket)
        self.client_socket.send(request.encode())

        # Receive the server's response
        reply = self.client_socket.recv(1024).decode()
        print(reply)
        if reply == "success":
            self.display_message("Inscription réussie")
        else:
            self.display_message("Échec de l'inscription")

    def display_message(self, message):
        # Display the message (you may customize this part based on your UI)
        print(message)


class LoginPage(QWidget):
    login_success_signal = pyqtSignal()

    def __init__(self, client_socket, chat_client):
        super().__init__()
        self.client_socket = client_socket
        self.chat_client = chat_client
        self.setWindowTitle("Connexion")
        self.resize(400, 300)

        # Create username and password input fields
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Create a login button
        self.login_button = QPushButton("Se connecter", self)
        self.login_button.clicked.connect(self.login)

        # Create a variable to indicate successful login
        login_success = False

        # Arrange elements in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def is_connected(self):
        try:
            # Send a ping message to the server
            request = f"ping".encode()
            self.client_socket.sendto(request, (host, port))

            # Set a timeout for receiving the reply
            socket.setdefaulttimeout(1)

            # Try to receive a reply from the server
            reply = self.client_socket.recvfrom(1024)

            # Reset the timeout to the original value
            socket.setdefaulttimeout(None)

            # If a reply was received, the connection is active
            if reply:
                return True
            else:
                return False
        except Exception as e:
            return False

    def login(self):
        try:
            # Check if the socket is connected to the server
            if self.client_socket.is_connected():
                # Send the login request to the server
                request = f"login {self.username_input.text()} {self.password_input.text()}"
                self.client_socket.send(request.encode())

                # Wait for the server's response
                reply = self.client_socket.recv(1024).decode()

                # If the login was successful, emit the login_success_signal
                if reply == "success":
                    self.display_message("Connexion réussie")
                    self.login_success_signal.emit()  # Emit the signal for successful login
                    self.close()  # Close the login page
                    self.chat_client.show()  # Show the ChatClient window
                else:
                    self.display_message("Échec de la connexion")
            else:
                print("La connexion au serveur est fermée")
        except Exception as e:
            print(f"An error occurred during login: {e}")


class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenue dans le chat")
        self.resize(400, 300)

        # Store the client socket for communication
        self.client_socket = socket.socket()

        # Afficher un message de bienvenue
        self.message_label = QLabel(self)
        self.message_label.setText("Bienvenue dans le chat !")

        # Créer un bouton de connexion
        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.login)

        # Créer un bouton d'inscription
        self.register_button = QPushButton("S'inscrire")
        self.register_button.clicked.connect(self.register)

        # Disposer les éléments
        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        self.chat_client = None  # Initialize to None
        self.login_page = None  # Initialize to None
        self.register_page = None  # Initialize to None

        try:
            self.client_socket.connect((host, port))
            self.chat_client = ChatClient(self.client_socket)
            self.login_page = LoginPage(self.client_socket, self.chat_client)
            self.login_page.login_success_signal.connect(self.on_login_success)
            self.register_page = RegisterPage(self.client_socket)
            self.chat_client.reception_thread.start()  # Start the receive_messages thread
        except ConnectionAbortedError as e:
            print(f"Connection aborted: {e}")
        except OSError as e:
            print(f"Connection error: {e}")

    def on_login_success(self):
        if self.login_page is not None:
            # Check if the login page is already closed
            if not self.login_page.isVisible():
                self.login_page.close()
        else:
            print("Login page not found")

        self.close()  # Close the welcome page

    def login(self):
        if self.login_page is not None:
            self.login_page.show()

    def register(self):
        # Ouvrir la page d'inscription
        if self.register_page is not None:
            self.register_page.show()

    def display_message(self, message):
        print(message)



class ChatThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        global flag
        try:
            while not flag:
                reply = self.client_socket.recv(1024).decode()
                if not reply:
                    break  # Exit the loop if the server connection is closed
                self.message_received.emit(reply)
                if reply == "stop":
                    break
        except Exception as e:
            print(f"Error in ChatThread: {e}")

        finally:
            self.client_socket.close()


class ChatClient(QWidget):
    def __init__(self, client_socket):
        super().__init__()
        self.setWindowTitle("Chat Client")
        self.resize(400, 300)
        self.client_socket = client_socket
        self.run_thread = True

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.message_input = QLineEdit(self)
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit_application)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_history)
        message_layout = QHBoxLayout()
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)
        layout.addLayout(message_layout)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        self.reception_thread = ChatThread(client_socket=self.client_socket)
        self.reception_thread.message_received.connect(self.display_message)
        self.reception_thread.start()

    def send_message(self):
        message = self.message_input.text()

        try:
            self.client_socket.send(message.encode())
            self.message_input.clear()
            self.chat_history.append("vous : " + message + "\n")

        except Exception as e:
            print(f"Error sending message: {e}")

    def quit_application(self):
        global flag

        try:
            # Send the stop signal to the server
            self.client_socket.send("stop".encode())

            # Set the flag to stop the reception thread
            flag = True

            # Stop the reception thread
            self.reception_thread.stop_thread()
            self.reception_thread.wait()

            # Close the socket and the ChatClient window
            self.client_socket.close()
            self.close()

        except Exception as e:
            print(f"Error closing connection: {e}")

    def display_message(self, message):
        self.chat_history.append(message + "\n")

if __name__ == "__main__":
    app = QApplication([])
    welcome_page = WelcomePage()
    welcome_page.show()
    app.exec()




