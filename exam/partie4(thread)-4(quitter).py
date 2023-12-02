from PyQt6.QtCore import Qt
import sys
import threading
from PyQt6.QtWidgets import (
  QApplication, QGridLayout, QWidget, QLabel, QPushButton,QLineEdit,QComboBox,QMessageBox
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Une Premiere fenêtre")
        self.etatunite = 0
        Grid = QGridLayout()
        self.setLayout(Grid)
        conteur = 0
        arret_thread = False

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
        global compteur,arret_thread
        while not arret_thread:
           compteur =+ 1
            self.affiche.setText(str(compteur))



    def start(self):
        compte = threading.Thread(target=self.__start)
        compte.start()


    def reset(self):
        compteur =0
        self.affiche.setText(str(compteur))

    def stop(self):
        global compte
        arret_thread = True
        compte.join()


    def quit(self):
        stop()
        QApplication.exit()




app = QApplication(sys.argv)
window = Window()
window.show()
if __name__ == '__main__':
   sys.exit(app.exec())