from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QBoxLayout
import sys
import random

class QuotApp (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор цитрат")
        
        self.resize(400, 150)
        self.qoutes = ["Будь собой", "Сегодня все будет хорошо", "Дрежи себя в руках"]
        self.btn = QPushButton("Показать цитату", self)
        self.label = QLabel("Нажми на кнопку", self)

        self.btn.clicked.connect(self.show_quote)

        layout = QBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def show_quote(self):
        self.label.setText(random.choice(self.qoutes))



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuotApp()
    window.show()
    sys.exit(app.exec())
