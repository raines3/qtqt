from PyQt6.QtWidgets import QHeaderView, QMainWindow, QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt6 import uic
import sys 
import sqlite3

class orion_dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("cosmo_dialog.ui", self) #подключение интерфейса
        self.db_name = "orion.db" # создание бд
        self.init_db()
        

        self.open_btn.clicked.connect(self.check_autho)

    def init_db(self): #функция инициализации базы данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
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
                            FOREIGN KEY (pilot_id) REFERENCES pilots(id) ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS infomation(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            age INTEGER NOT NULL,
                            exp INTEGER NOT NULL,
                            bio TEXT NOT NULL,
                            pilot_id INTEGER,
                            FOREIGN KEY (pilot_id) REFERENCES pilots(id) ON DELETE CASCADE)""")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users(role, password) VALUES (?, ?)", ("диспетчер", "123"))
            cursor.execute("INSERT INTO users(role, password) VALUES (?, ?)", ("координатор", "222"))
            
            test_pilots = [("В.А Камаров", "Доступен"),  #sp = [1,2]    x,a = sp sp = [(1,2),(1,2)]
                           ("Н.П. Филипов", "Доступен")] 
            
            for p in test_pilots:
                    cursor.execute("INSERT INTO pilots(name, status) VALUES (?, ?)", (p[0],p[1]))


     
        
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
        print(res, role, password )
        conn.close()

        if res and res[0] == password:
            self.user_role = role
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный ключ доступа")
        
        self.password_input.clear()


class Orion_main(QMainWindow): #основное окно
    def __init__(self, role, db_name): #инициализация окна
        super().__init__()
        uic.loadUi("cosmo_main.ui", self) #подключение интерфейса
        self.user_role = role
        self.db_name = db_name
        self.label.setText(f"Активная сессия {self.user_role}")
        self.refresh_all()
        if self.user_role == "диспетчер":
            self.admin.setVisible(False)
        
        self.start_btn.clicked.connect(self.on_add)
        self.close_btn.clicked.connect(self.close)
        self.new_btn.clicked.connect(self.new_pilot)
        self.del_btn.clicked.connect(self.on_delete)
        self.change_btn.clicked.connect(self.change_status)

    def refresh_all(self):
        self.flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Обновление комбобокса с пилотами
            cursor.execute("SELECT id, name FROM pilots WHERE status = 'Доступен' ORDER BY name")
            pilots = cursor.fetchall()
            print(f"Найдено пилотов: {len(pilots)}")  # Отладка
            
            self.combo_pilots.clear()
            self.combo_pilots.addItem("Выберите пилота")
            for pilot_id, name in pilots:
                self.combo_pilots.addItem(name, pilot_id)  # Используйте addItem с данными
            
            # Получение рейсов
            cursor.execute("""SELECT flights.id,flights.pilot_id, flights.destination,flights.weight, flights.status
                            FROM flights 
                            LEFT JOIN pilots ON flights.pilot_id = pilots.id 
                            ORDER BY flights.id DESC""")
            flights = cursor.fetchall()
            print(f"Найдено рейсов: {len(flights)}")  # Отладка
            
            # Настройка таблицы
            self.flight_table.setRowCount(len(flights))
            self.flight_table.setColumnCount(5)  # Убедитесь, что 4 колонки
            
            for row, flight in enumerate(flights):
                for col, val in enumerate(flight):
                    item = QTableWidgetItem(str(val))
                    self.flight_table.setItem(row, col, item)
            
            conn.close()
            
        except Exception as e:
            print(f"Ошибка в refresh_all: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные: {e}")

            

       

         
    def on_add(self): #добавление нового полета
        dest = self.dest_input.text().strip()
        weight_text = self.weight_input.text().strip()
        pilot_id = self.combo_pilots.currentText()
        print(dest,pilot_id,weight_text)

        if not dest or not weight_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        try:
            weight = float(weight_text)
        
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Вес должен быть числом")
            return

        if pilot_id is None or pilot_id == "" :
            QMessageBox.warning(self, "Ошибка", "Нет доступных пилотов")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
    
        cursor.execute('INSERT INTO flights(destination,weight,pilot_id,status) VALUES (?, ?, ?,?)', (dest, weight_text, pilot_id,"Назначен"))
        conn.commit()
        conn.close()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE pilots SET status = 'В рейсе' WHERE name = ?", (pilot_id,))
        conn.commit()
        conn.close()



        self.dest_input.clear()
        self.weight_input.clear()

        self.refresh_all()

    def change_status(self):
        current_row = self.flight_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите рейс")
            return
        
        flight_id = int(self.flight_table.item(current_row, 0).text())
        current_status = self.flight_table.item(current_row, 4).text()

        new_status = "Назначен" if current_status == "Формируется" else "Формируется"
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE flights SET status = ? WHERE id = ?", (new_status, flight_id))
        conn.commit()
        conn.close()
        self.refresh_all()
    
    def new_pilot(self):
        pilot_name = self.pilot_name_input.text().strip()
        if not pilot_name:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО пилота")
            return
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pilots (name, status) VALUES (?, ?)", (pilot_name, "Доступен"))
        conn.commit()
        conn.close()

        self.pilot_name_input.clear()

        self.refresh_all()

        QMessageBox.information(self, "Успешно", f"Добавлен пилот: {pilot_name}")

    def on_delete(self):
        current_row = self.flight_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберете рейс для удаления")
            return
        
        flight_id = int(self.flight_table.item(current_row, 0).text())

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor() 
        cursor.execute("SELECT pilot_id FROM flights WHERE id = ?", (flight_id,))
        res = cursor.fetchone()
        if res and res[0]:
            cursor.execute("UPDATE pilots SET status = 'Доступен' WHERE id = ?", (res[0],))
        
        cursor.execute("DELETE FROM flights WHERE id = ?", (flight_id, ))
        conn.commit()
        conn.close()
        self.refresh_all()
 
class Info_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("orion_info_dialog.ui", self)
    
    def show_info(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""SELECT infomation.id, infomation.age, infomation.exp, infomation.bio, infomation.pilot_id
                            FROM infomation
                            JOIN pilots ON infomation.pilot_id = pilots.id
                            ORDER BY infomation.id""")
        info = cursor.fetchall()
        self.age_label.addText(f"Возраст: {info[1]}")
        self.exp_label.addText(f"Стаж: {info[2]}")
        self.bio_label.addText(f"Биография: {info[3]}")
        self.info_label.addTetx(f"Информация о: {info[4]}")

    

        
        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""QDialog, QMainWindow {
                        background-color: #121824;}
                        QLabel {
                        color: #00ffcc;
                        }
                        QLineEdit, QComboBox {
                        background-color: #21262d;
                        color: #0077ff;
                        border: 1px solid #30363d;}
                        QPushButton {
                        background-color: #233863;
                        color: #ffffff;}
                        QTableWidget {
                        background-color: #0d1117;
                        color: #c9d1d9;
                        border: 1px solid #30363d;}""")
    
    while True:

        dialog = orion_dialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            role = dialog.user_role
            db_name = dialog.db_name
            
        
            window = Orion_main(role, db_name)
            window.show()
            app.exec()

            continue
        else:
            break
    sys.exit(0)


          

