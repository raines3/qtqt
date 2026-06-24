import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt

class CyberWarehouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("warehouse.ui",self)
        self.db_name = "storage.db"
        self.init_daatabase()
        self.add_btn.clicked.connect(self.add_implant)
        self.load_data_from_db()

    def init_daatabase(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute('''
                 CREATE TABLE IF NOT EXISTS implants (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT NOT NULL,
                                  category TEXT NOT NULL, 
                                  quantity INTEGER DEFAULT 0
                                  )
                                  ''')
    def load_data_from_db(self):
        self.tableWidget.setRowCount(0)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, category, quantity FROM implants")
            rows = cursor.fetchall()

            for row_idx, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))

                    if col_idx in (0, 3):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    self.tableWidget.setItem(row_idx, col_idx, item)

    def add_implant(self):
        name = self.name_input.text().strip()
        category = self.catagory_input.text().strip()
        qty = self.qty_input.text().strip()

        if not name or not category or not qty.isdigit():
            return
        
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute(
                "INSERT INTO implants (name, category, quantity) VALUES (?, ?, ?)",
                (name, category, int(qty))
            )
        self.name_input.clear()
        self.catagory_input.clear()
        self.qty_input.clear()

        self.load_data_from_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberWarehouseApp()
    window.show()
    sys.exit(app.exec())