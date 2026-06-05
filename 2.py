from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QBoxLayout, QLineEdit
import sys
import random

class ParcentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Процентный калькулятор")
        self.resize(300, 200)

        self.num_input = QLineEdit(self)
        self.num_input.setPlaceholderText("Число")
        self.btn = QPushButton(self)
        self.label = QLabel(self)

        layout = QBoxLayout()
        layout.addWidget(self.num_input)
        layout.addWidget(self.layoutbtn)
        layout.addWidget(self.label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuotApp()
    window.show()
    sys.exit(app.exec())
