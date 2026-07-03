from PyQt6.QtWidgets import QMainWindow, QDialog, QApplication, QMessageBox
from PyQt6 import uic
import sys 
import sqlite3

class cosmos(QDialog):
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
                            name TEXT NOT NULL
                            )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS flights(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            planet TEXT NOT NULL,
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
        
        self.pushButton_3.clicked.connect(self.on_add)

    def on_add(self):
        

