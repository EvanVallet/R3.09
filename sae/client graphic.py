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
)

flag = False
host = "127.0.0.1"
port = 11111
client_socket = socket.socket()


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
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
    client = ChatClient()
    client.show()
    app.exec()
