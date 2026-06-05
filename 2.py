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
        self.num_input2 = QLineEdit(self)
        self.btn = QPushButton(self)
        self.label = QLabel(self)

        self.btn.clicked.connect(self.calculate)

        layout = QBoxLayout()
        layout.addWidget(self.num_input)
        layout.addWidget(self.layoutbtn)
        layout.addWidget(self.label)

    def calculate(self):
        res = self.num_input + self.num_input2
        self.label.setText(f"{res}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParcentApp()
    window.show()
    sys.exit(app.exec())
