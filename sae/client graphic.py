#sqlalchemi
import socket
import threading
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

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket  # Set the client socket
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



        # Arrange elements in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Send a login request to the server
        request = f"login {username} {password}"
        self.client_socket.send(request.encode())

        # Receive the server's response
        reply = self.client_socket.recv(1024).decode()
        if reply == "success":
            self.display_message("Connexion réussie")

            client = ChatClient()
            client.show()
        else:
            self.display_message("Échec de la connexion")







class WelcomePage(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenue dans le chat")
        self.resize(400, 300)

        # Store the client socket for communication
        self.client_socket = client_socket

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

        # Create instances of other pages but don't show them yet
        self.login_page = LoginPage(self.client_socket)
        self.register_page = RegisterPage(self.client_socket)
        try:
            self.client_socket.connect((host, port))
        except ConnectionAbortedError:
            self.display_message("Connection aborted")
        except OSError:
            self.display_message("Connection error")

    def login(self):
        # Ouvrir la page de connexion
        self.login_page.show()


    def register(self):
        # Ouvrir la page d'inscription
        self.register_page.show()





class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Client")
        self.resize(400, 300)
        self.client_socket = socket.socket

        # Create the page of welcome with the client_socket



        # Afficher la page de bienvenue
        self.welcome_page.show()
        self.setWindowTitle("Chat Client")
        self.resize(400, 300)
        self.client_socket = socket.socket()

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

        try:
            self.client_socket.connect((host, port))
            self.reception_thread = threading.Thread(target=self.receive_messages)
            self.reception_thread.start()
        except ConnectionAbortedError:
            self.display_message("Connection aborted")
        except OSError:
            self.display_message("Connection error")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Send a login request to the server
        request = f"login {username} {password}".encode()
        self.client_socket.send(request)

        # Receive the server's response
        reply = self.client_socket.recv(1024).decode()
        if reply == "success":
            self.is_logged_in = True
            self.display_message("Connexion réussie")
        else:
            self.display_message("Échec de la connexion")

    def send_message(self):
        message = self.message_input.text()
        self.client_socket.send(message.encode())
        self.message_input.clear()
        self.chat_history.append("vous : "+ message + "\n")

    def quit_application(self):
        global flag

        self.client_socket.send("stop".encode())
        flag = True
        self.client_socket.close()
        self.close()

    def receive_messages(self):
        global flag
        while not flag:
            try:
                reply = self.client_socket.recv(1024).decode()
                self.display_message(reply)
                if reply == "stop":
                    self.client_socket.close()
                    flag = True

            except ConnectionAbortedError:
                self.display_message("Connection lost")
                flag = True

    def display_message(self, message):
        self.chat_history.append(message + "\n")


if __name__ == "__main__":
    app = QApplication([])
    welcome_page = WelcomePage()
    welcome_page.show()
    app.exec()


