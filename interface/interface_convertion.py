from PyQt6.QtCore import Qt
import sys
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

    temperature= QLabel("Temperature")
    Grid.addWidget(temperature,0,0,1,1)
    self.unite= QLabel("C")
    Grid.addWidget(self.unite,0,3,1,5)

    self.input = QLineEdit()

    Grid.addWidget(self.input,0,1,1,1)

    self.retour = QLineEdit()
    Grid.addWidget(self.retour,2,1,1,5)
    self.retour.setEnabled(False)

    buttonok = QPushButton("ok")
    buttonok.clicked.connect(self.get)
    Grid.addWidget(buttonok,1,1,1,4)

    self.combo = QComboBox(self)
    self.combo.addItem("C->K")
    self.combo.addItem("K->C")
    self.combo.currentIndexChanged.connect(self.index_change)
    Grid.addWidget(self.combo,1,5,1,2)

    button = QPushButton("Quitter")
    button.clicked.connect(self.quit)
    Grid.addWidget(button,3,1,1,3)

    buttonok = QPushButton("?")
    buttonok.clicked.connect(self.help)
    Grid.addWidget(buttonok, 3, 4,1,2)


  def help(self):
    message="Permet de convertir un nombre de Kelvins en Celcius et vice-versa"
    QMessageBox.information(self,"aide",message,QMessageBox.StandardButton.Ok)

  def get(self):
      try:
        envoi = float(self.input.text())
      except ValueError:
        retour = "uniquement des nombres pris en compte"
        print(retour)
        self.retour.setText(str(retour))
      else:
        test=self.etatunite
        print(self.etatunite)
        if test == 1 and envoi >= 0:
            retour = envoi - 273.15
            print(retour)
            self.retour.setText(str(retour))

        elif test == 0 and envoi > -273.15:
            retour = envoi + 273.15
            print(retour)
            self.retour.setText(str(retour))
        else:
              retour = "inferieur au zero absolu"
              print(retour)
              self.retour.setText(str(retour))

  def index_change(self, index):
    print("Index changed", index)
    if index == 1:
      self.unite.setText("K")
      self.etatunite = 1
    if index == 0:
      self.unite.setText("°C")
      self.etatunite = 0
  

  def quit(self):
    self.close()


app = QApplication(sys.argv)
window = Window()
window.show()
if __name__ == '__main__':
   sys.exit(app.exec())
