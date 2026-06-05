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
        self.perc_input = QLineEdit(self)
        self.perc_input.setPlaceholderText("Процент")

        self.btn = QPushButton("Посчитать", self)
        self.label = QLabel("Результат: ", self)

        self.btn.clicked.connect(self.calculate)

        layout = QBoxLayout()
        layout.addWidget(self.num_input)
        layout.addWidget(self.perc_input)
        layout.addWidget(self.layoutbtn)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def calculate(self):
        res = float(self.num_input.text()) * float(self.perc_input.text())/100
        self.label.setText(f"Результат: {res}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParcentApp()
    window.show()
    sys.exit(app.exec())
