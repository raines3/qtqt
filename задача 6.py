"""
ЗАДАЧА С-2: «Конвертер валют» (Уровень: Средний)

ОПИСАНИЕ:
Конвертация введенной суммы в валюту (USD или EUR) по курсу.

ТРЕБОВАНИЯ К ИНТЕРФЕЙСУ (UI):
1. Виджеты: 
   - QLineEdit (имя: 'sum_input'),
   - QComboBox (имя: 'currency_box' с элементами "USD", "EUR"),
   - QPushButton (имя: 'calc_btn'),
   - QLabel (имя: 'res_label').

ТРЕБОВАНИЯ К GIT:
1. Создайте дизайн .ui: git commit -m "layout: верстка конвертера"
2. Логика пересчета: git commit -m "feat: логика пересчета курса"
"""

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QBoxLayout, QMainWindow
from PyQt6 import uic
import sys

class Currency_converter(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi("6.ui", self)
      items = ["USD", "EUR"]
      self.currency_box.addItems(items)

      self.calc_btn.clicked.connect(self.con)

   def con(self):
      if self.currency_box.currentText() == "USD":
         res = float(self.sum_input.text()) /  71.73
         self.res_label.setText(f"Результат: {res}")
      elif self.currency_box.currentText() == "EUR":
         res = float(self.sum_input.text()) /  82.78
         self.res_label.setText(f"Результат: {res}")
         print(res)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Currency_converter()
    window.show()
    sys.exit(app.exec())