"""
ЗАДАЧА С-1: «Авторизация» (Уровень: Средний)

ОПИСАНИЕ:
Создайте окно логина, проверяющее введенные данные.

ТРЕБОВАНИЯ К ИНТЕРФЕЙСУ (UI):
1. В Qt Designer создайте Main Window.
2. Добавьте: 
   - QLineEdit с именем 'login_input',
   - QLineEdit с именем 'pass_input' (режим Password),
   - QPushButton с именем 'login_btn'.
3. Имена виджетов должны совпадать с кодом!

ТРЕБОВАНИЯ К GIT:
1. Создайте дизайн .ui: git commit -m "layout: создан дизайн авторизации"
2. Добавьте проверку: git commit -m "feat: добавлена проверка логина и пароля"
"""

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QBoxLayout, QMainWindow
from PyQt6 import uic
import sys

class ui(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Авторизация")
      uic.loadUi("avt.ui", self)
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ui()
    window.show()
    sys.exit(app.exec())

