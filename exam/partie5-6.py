from PyQt6.QtCore import Qt
import sys
import threading
import socket
from PyQt6.QtWidgets import (
    QApplication, QGridLayout, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox
)

host = "127.0.0.1"
port = int(sys.argv[1])
client_socket = socket.socket()
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Une Premiere fenêtre")
        self.etatunite = 0
        Grid = QGridLayout()
        self.setLayout(Grid)
        global compteur, arret_thread, debut, connecte
        compteur = 0
        arret_thread = False
        debut=True
        connecte = False
        global connecte
        Compteur = QLabel("Compteur")
        Grid.addWidget(Compteur, 0, 0, 1, 1)

        self.affiche = QLineEdit()
        Grid.addWidget(self.affiche, 0, 0, 2, 1)
        self.affiche.setEnable(False)

        buttonstart = QPushButton("start")
        buttonstart.clicked.connect(self.start)
        Grid.addWidget(buttonstart, 0, 0, 3, 1)

        buttonreset = QPushButton("reset")
        buttonreset.clicked.connect(self.reset)
        Grid.addWidget(buttonreset, 0, 0, 4, 2)

        buttonstop = QPushButton("stop")
        buttonreset.clicked.connect(self.stop)
        Grid.addWidget(buttonstop, 0, 0, 4, 2)

        buttonconnect = QPushButton("stop")
        buttonconnect.clicked.connect(self.connect)
        Grid.addWidget(buttonconnect, 0, 0, 4, 2)

        buttonquitter = QPushButton("stop")
        buttonquitter.clicked.connect(self.quit)
        Grid.addWidget(buttonquitter, 0, 0, 4, 2)

    def __start(self):
        global compteur, arret_thread , connecte
        while not arret_thread:
            compteur = + 1
            self.affiche.setText(str(compteur))
            if connecte:
                message = compteur
                client_socket.send(message.encode())


    def start(self):
        compte = threading.Thread(target=self.__start)
        global debut, connecte
        if connecte:
            message = "start"
            client_socket.send(message.encode())
        if debut:
            compte.start()
            debut=False



    def reset(self):
        compteur = 0
        self.affiche.setText(str(compteur))
        if connecte:
            message = "reset"
            client_socket.send(message.encode())


    def stop(self):
        global compte , debut , arret_thread, connecte
        arret_thread = True
        compte.join()
        debut = True
        if connecte:
            message = "stop"
            client_socket.send(message.encode())

    def connect(self):
        global connecte
        try:
            client_socket.connect((host,port))
            connecte =True
        except ConnectionError:
            print("le serveur n'est pas joignable")
        except ConnectionAbortedError:
            print("arret de la connexion")

        except OSError:
            print("arret de la connexion")


    def quit(self):
        global connecte
        if connecte:
            message = "quitter"
            client_socket.send(message.encode())
            message = "bye"
            client_socket.send(message.encode())
        self.stop()
        QApplication.exit()


app = QApplication(sys.argv)
window = Window()
window.show()
if __name__ == '__main__':
    sys.exit(app.exec())