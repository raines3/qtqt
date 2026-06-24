"""
НАЗВАНИЕ ЗАДАЧИ: Журнал бортового самописца «Chronos»

ПРИНЦИП РАБОТЫ ПРОГРАММЫ:
1. Привязка к календарю: Таблица 'log_table' отображает записи не за всё время, а строго за тот день,
   который выбран пользователем в виджете календаря 'calendar'.
2. Динамическое обновление при клике: Календарь посылает сигнал .selectionChanged при каждом клике на новую дату.
   Программа перехватывает этот сигнал, считывает выбранную дату в формате строки "yyyy-MM-dd", делает SQL-запрос
   с фильтрацией WHERE date = ? и мгновенно перерисовывает таблицу.
3. Добавление записи: Оператор выбирает дату на календаре, указывает тип происшествия в выпадающем списке 'combo_box',
   вводит текст сообщения в 'log_input' и нажимает 'save_btn'. Запись улетает в базу и привязывается к выбранному числу.
"""

import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic

class SpaceLogApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("chronos.ui", self)
        self.db_name = "chronos.db"
        self.init_db()
        self.calendar.selectionChanged.connect(self.refresh_logs)
        self.save_btn.clicked.connect(self.add_entry)
        self.refresh_logs()

        # TODO: Вызвать метод инициализации БД self.init_db()
        # TODO: Связать сигнал изменения даты в календаре (self.calendar.selectionChanged) с методом self.refresh_logs
        # TODO: Привязать клик по кнопке save_btn к методу self.add_entry
        # TODO: Показать логи на текущую дату календаря, запустив self.refresh_logs()
        

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute(
                """CREATE TABLE IF NOT EXISTS logs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    event_type TEXT,
                    message TEXT)"""
                )
            conn.commit() 
        self.refresh_logs()
        # TODO: Создать таблицу logs (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, event_type TEXT, message TEXT)
        

    def refresh_logs(self):
        current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.log_table.setRowCount(0)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id,date,event_type,message FROM logs WHERE date = ?", (current_date, ))
            rows = cursor.fetchall() 
            for row_idx, data in enumerate(rows):
                self.log_table.insertRow(row_idx)
                for col_idx, val in enumerate(data):
                    item = QTableWidgetItem(str(val))
                    self.log_table.setItem(row_idx, col_idx ,item)



                


            


        # TODO: Получить выбранную дату из календаря: current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        # TODO: Очистить таблицу на экране через setRowCount(0)
        # TODO: Выбрать из БД записи, где поле date равно current_date, и циклом заполнить таблицу log_table
        

    def add_entry(self):
        current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        sel_combo = self.comboBox.currentText()
        sel_input = self.log_input.text().strip()
        if sel_input:
            with sqlite3.connect(self.db_name) as conn:
                conn.cursor().execute("INSERT INTO logs (date,event_type, message) VALUES (?, ?, ?)",( current_date,sel_combo,sel_input ))
                conn.commit() 
        self.log_input.clear()
        self.refresh_logs()
            
        
        # TODO: Получить выбранную дату из календаря в формате "yyyy-MM-dd"
        # TODO: Считать выбранный текст из combo_box и текст лога из log_input (удалить пробелы)
        # TODO: Если поле сообщения не пустое -> записать данные через INSERT INTO в БД
        # TODO: Очистить текстовое поле log_input и вызвать метод self.refresh_logs() для обновления экрана
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpaceLogApp()
    window.show()
    sys.exit(app.exec())