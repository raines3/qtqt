from PyQt6.QtWidgets import QApplication, QDialog, QWidget, QPushButton, QLabel, QBoxLayout, QMainWindow
from PyQt6 import uic
import sys


class CharacterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("dialog.ui", self)
        self.horizontalSlider.valueChanged .connect(self.progressBar.setValue)
        self.horizontalSlider_2.valueChanged.connect(self.progressBar_2.setValue)
    
    def get_charter_data(self):
       char_class = self.comboBox.currentText()
       strength = self.horizontalSlider.value()
       agility = self.horizontalSlider_2.value()
       return char_class, strength, agility



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_win.ui", self)
        self.pushButton.clicked.connect(self.open_creater)

    def open_creater(self):
        dialog = CharacterDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            char_class, strength, agility = dialog.get_charter_data()

            self.label.setText(f"Класс: {char_class}")
            self.label_2.setText(f"Класс: {strength}")
            self.label_3.setText(f"Класс: {agility}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



