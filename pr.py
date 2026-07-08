from PyQt6.QtWidgets import QMainWindow, QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt6 import uic
import sys 
import sqlite3

class orion_dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("cosmo_dialog.ui", self)
        self.db_name = "orion.db"
        self.init_db()

    def init_db(self): #функция инициализации базы данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_key = ON")
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            role TEXT NOT NULL,
                            password TEXT NOT NULL)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS pilots(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            status TEXT NOT NULL
                            )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS flights(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            destination TEXT NOT NULL,
                            weight INTEGER NOT NULL,
                            status TEXT NOT NULL,
                            pilot_id INTEGER,
                            FOREIGHT KEY (pilot_id) REFERENCES pilots(id) ON DELETE CASCADE
                            )""")
        
        cursor.execute("SELECT COUNT(*) ")
        conn.commit()
        conn.close()


    def check_autho(self): #проверка аторизации
        role = self.combobox.currentText()
        password = self.password_input.text().strip()

        if password == "":
            QMessageBox.warning(self, "Ошибка", "Введите секретный ключ")
            return
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE role = ?", (role, ))
        res = cursor.fetchone()
        conn.close()

        if res and res[0] == password:
            self.user_role = role
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный ключ доступа")
        
        self.password_input.clear()


class Orion_main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("cosmo_main.ui", self)
        self.label.setText(f"Активная сессия {self.user_role}")
        if self.user_role == "Диспетчер":
            self.admin.setVisible(False)
        
        self.start_btn.clicked.connect(self.on_add)

    def refresh_all(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM pilots WHERE status = 'Доступно' ORDER BY name")

        pilots = cursor.fetchall()

        for id, name in pilots:
            self.combo_pilots.setItem()
        

        cursor.execute("SELECT f.id, f.destination, f.weight, f.status, COALESCE(p.name, 'Не назначен') as pilot_name FROM flights f JOIN pilots p ON f.pilots_id = p.id ORDERA BY f.id DESC")
        flights = cursor.fetchall()

        self.flight_table.setRowCount(len(flights))

        for row, flight in enumerate(flights):
            for col, val in enumerate(flight):
                item = QTableWidgetItem(str(val))

                if col == 2:
                    item.setText(f'{val} т')
                
                self.flight_table.setItem(row, col, item)
            

       

        
    def on_add(self):
        dest = self.dest_input.text().strip()
        weight_text = self.weight_input.text().strip()
        pilot_id = self.combo_pilots.currentData()

        if not dest or not weight_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        try:
            weight = float(weight_text)
        
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Вес должен быть числом")
            return

        if pilot_id is None:
            QMessageBox.warning(self, "Ошибка", "Нет доступных пилотов")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM pilots WHERE id = ?")
        cursor.execute('INSERT INTO flights(planet,weight,pilot_id) VALUES (?, ?, ?)', (dest, weight_text, pilot_id))
        cursor.execute("UPDATE pilots SET status = 'В рейсе' WHERE id = ?", (pilot_id,))
        conn.commit()
        conn.close()

        self.dest_input.clear()
        self.weight_input.clear()


if __name__ == "__main__":
    pass