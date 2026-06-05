from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QBoxLayout, QMainWindow
from PyQt6 import uic
import sys
import random
class Change(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.pushButton_2.clicked.connect(lambda: self.setStyleSheet("background-color:green;"))
        self.pushButton.clicked.connect(lambda: self.setStyleSheet("background-color:red;"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Change()
    window.show()
    sys.exit(app.exec())
