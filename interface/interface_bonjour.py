from PyQt6.QtCore import Qt
import sys
from PyQt6.QtWidgets import (
  QApplication, QGridLayout, QWidget, QLabel, QPushButton,QLineEdit
)



class Window(QWidget):
  def __init__(self):
    super().__init__()
    self.resize(300, 250)
    self.setWindowTitle("Une Premiere fenêtre")

    Grid = QGridLayout()
    self.setLayout(Grid)

    self.input = QLineEdit()
    Grid.addWidget(self.input,0,1)

    self.retour = QLabel()
    Grid.addWidget(self.retour,2,1)

    buttonok = QPushButton("ok")
    buttonok.clicked.connect(self.get)
    Grid.addWidget(buttonok,1,1)

    button = QPushButton("Quitter")
    button.clicked.connect(self.quit)
    Grid.addWidget(button,3,1)

  def get(self):
    text = "boujour " + self.input.text()
    self.retour.setText(text)
    print(text)

  def quit(self):
    self.close()


app = QApplication(sys.argv)
window = Window()
window.show()
if __name__ == '__main__':
   sys.exit(app.exec_())
