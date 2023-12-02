from PyQt6.QtCore import Qt
import sys
from PyQt6.QtWidgets import (
  QApplication, QGridLayout, QWidget, QLabel, QPushButton,QLineEdit,QComboBox,QMessageBox
)

class windows():
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Une Premiere fenêtre")
        self.etatunite = 0
        Grid = QGridLayout()
        self.setLayout(Grid)
        conteur = 0

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

    def start(self):
        compteur =+ 1
        self.affiche.setText(str(compteur))

    def reset(self):
        compteur =0
        self.affiche.setText(str(compteur))

    def quit(self):
        self.close()
