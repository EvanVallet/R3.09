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
    QCheckBox
)

flag = False
trea = False
host = "127.0.0.1"
port = 11111
client_socket = socket.socket()


class start(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenue dans le chat")
        self.resize(400, 300)
        self.client_socket = socket.socket()

        # Créer un bouton de connexion
        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.login)

        # Créer un bouton d'inscription
        self.register_button = QPushButton("S'inscrire")
        self.register_button.clicked.connect(self.register)

        # Disposer les éléments
        layout = QVBoxLayout()
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        self.Login=login()
        self.Register = register()


    def login(self):

        self.Login.show()


    def register(self):
        self.Register.show()




class login(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket
        self.setWindowTitle("Connexion")
        self.resize(400, 300)
        print("d")
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

        self.Run = ChatClient()

    def login(self):
        logins= f"login {self.username_input.text()} {self.password_input.text()}"
        client_socket.send(logins.encode())
        recu = client_socket.recv(1024).decode()
        if recu == "success":
            print("connexion réusssi")
            self.Run.show()


class register(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket  # Set the client socket

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
        registers = f"register {username} {password}"
        client_socket.send(registers.encode())
        recu = client_socket.recv(1024).decode()
        if recu == "success":
            print("connexion réusssi")
            start.show()

class rooms(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket  # Set the client socket

        self.setWindowTitle("Inscription")
        self.resize(400, 300)

        # Liste des noms de salons
        room_names = ["Blabla", "Comptabilité", "Informatique", "Marketing"]

        # Création des cases à cocher pour chaque salon
        self.checkboxes = {name: QCheckBox(name) for name in room_names}

        # Bouton pour se connecter aux salons sélectionnés
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_to_selected_rooms)

        # Layout
        layout = QVBoxLayout(self)
        for checkbox in self.checkboxes.values():
            layout.addWidget(checkbox)
        layout.addWidget(connect_button)

    def connect_to_selected_rooms(self):
        selected_rooms = [name for name, checkbox in self.checkboxes.items() if checkbox.isChecked()]
        print("Connecting to rooms:", selected_rooms)
        self.client_socket.send(selected_rooms.encode())
        reply = self.client_socket.recv(1024).decode()


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Client")
        self.resize(400, 300)
        self.client_socket = socket.socket()

        self.roomsbutton = QPushButton
        self.roomsbutton.clicked.connect(self.rooms)

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

    def rooms(self):
        rooms.show()


    def send_message(self):
        message = self.message_input.text()
        self.client_socket.send(message.encode())
        self.message_input.clear()
        self.chat_history.append("vous : " + message + "\n")

    def quit_application(self):
        global flag

        self.client_socket.send("server/stop".encode())
        flag = True
        self.client_socket.close()
        self.close()

    def receive_messages(self):
        global flag
        while not flag:
            try:
                reply = self.client_socket.recv(1024).decode()
                self.display_message(reply)
                if reply == "server/stop":
                    self.client_socket.close()
                    self.close()
                    flag = True

            except ConnectionAbortedError:

                self.display_message("Connection lost")
                flag = True

    def display_message(self, message):
        if not message.startswith("server/"):
            self.chat_history.append(message + "\n")


if __name__ == "__main__":
    app = QApplication([])
    try:
        client_socket.connect((host, port))
        Start=start()
        Start.show()
        app.exec()
    except Exception as e:
        print(f"connexion: {e}")


