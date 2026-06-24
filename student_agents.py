"""
НАЗВАНИЕ ЗАДАЧИ: Картотека секретных агентов

ПРИНЦИП РАБОТЫ ПРОГРАММЫ:
1. Инициализация: При старте приложения автоматически создается база данных 'agents.db'
   и таблица 'agents' (если их еще нет). Поле 'clearance' (уровень допуска) должно быть целочисленным.
2. Добавление агента: Оператор вводит позывной в 'codename_input' и уровень допуска в 'clearance_input'.
   Программа проверяет, что поля не пустые, а допуск — это число. Новый агент всегда сохраняется
   в базу со статусом "Активен" по умолчанию.
3. Удаление: Оператор кликает по любой ячейке нужного агента в таблице 'agents_table' и нажимает 'delete_btn'.
   Программа считывает ID из первой колонки (индекс 0) и удаляет эту строку из SQLite.
4. Полная очистка (Nuke): При нажатии на 'nuke_btn' программа должна запросить подтверждение через
   QMessageBox.question. Если пользователь отвечает "Да" (Yes), база данных полностью стирает всех агентов.
"""

import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt

class AgentsManager(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("agents.ui", self)
        self.db_name = "agents.db"
        self.init_db()
        self.add_btn.clicked.connect(self.save_agent)
        self.delete_btn.clicked.connect(self.delete_selected_agent)
        self.nuke_btn.clicked.connect(self.nuke_database)

        # TODO: Вызвать метод self.init_db() для создания базы данных
        # TODO: Привязать обработчики кликов кнопок (add_btn, delete_btn, nuke_btn) к соответствующим методам
        # TODO: Вызвать метод self.refresh_table() для первичной загрузки данных в таблицу

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute(""" 
                CREATE TABLE IF NOT EXISTS agents(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codename TEXT NOT NULL,
                    status TEXT NOT NULL,
                    clearance INTEGER NOT NULL)
                                  """)
        self.refresh_table()

        # TODO: Написать SQL-запрос CREATE TABLE IF NOT EXISTS для таблицы agents
        # Поля: id (INTEGER PRIMARY KEY AUTOINCREMENT), codename (TEXT), status (TEXT), clearance (INTEGER)

    def refresh_table(self):
        # TODO: Очистить таблицу на экране через self.agents_table.setRowCount(0)
        # TODO: Сделать запрос "SELECT id, codename, clearance, status FROM agents"
        # TODO: Через цикл вставить строки (.insertRow) и заполнить ячейки элементами QTableWidgetItem
        self.agents_table.setRowCount(0)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id,  codename, status, clearance  FROM agents")
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.agents_table.insertRow(row_idx)
            for col_idx, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                if col_idx in (0, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.agents_table.setItem(row_idx, col_idx ,item)




    def save_agent(self):
        codename_input = self.codename_input.text().strip()
        status_input = self.status_input.text().strip()
        clearance_input = self.clearance_input.text().strip()
        if not codename_input or not status_input or not clearance_input.isdigit():
            QMessageBox.warning(self, "ошибка", "Заполните все поля для ввода и уровень доступа должен быть числом")
            return
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute("INSERT INTO agents (codename, status,clearance ) VALUES (?, ?, ?)", (codename_input, status_input, int(clearance_input)))
        
        self.codename_input.clear()
        self.status_input.clear()
        self.clearance_input.clear()
        self.refresh_table()





        # TODO: Считать поля ввода, убрать пробелы через .strip()
        # TODO: Валидация: поля не пустые, а clearance состоит только из цифр (.isdigit())
        # TODO: Выполнить INSERT запрос в БД (статус по умолчанию — 'Активен'), очистить поля ввода, обновить таблицу
    

    def delete_selected_agent(self):
        # TODO: Определить текущую выделенную строку через self.agents_table.currentRow()
        # TODO: Проверить, выбрана ли строка (индекс >= 0), если нет — показать предупреждение QMessageBox.warning
        # TODO: Получить ID агента из ячейки (строка, колонка 0) через метод .item(row, 0).text()
        # TODO: Выполнить SQL-запрос DELETE FROM agents WHERE id = ? и обновить таблицу
        row = self.agents_table.currentRow()
        if not row >= 0:
            QMessageBox.warning(self, "ошибка", "выберете строку для удаления")
        else:
            id = self.agents_table.item(row, 0).text()
            with sqlite3.connect(self.db_name) as conn:
                conn.cursor().execute("DELETE FROM agents WHERE id = ?", (id, ))
            self.refresh_table()
            
            


        

    def nuke_database(self):
        QMessageBox.question(self, "Внимание", "Удалитб ВСЕХ агентов")
        if QMessageBox.StandardButton.Yes:
             with sqlite3.connect(self.db_name) as conn:
                
                conn.cursor().execute("DELETE FROM agents")
                conn.commit()
                self.refresh_table()

            

        # TODO: Вызвать диалоговое окно подтверждения QMessageBox.question(self, "Внимание", "Удалить ВСЕХ агентов?")
        # TODO: Если пользователь ответил QMessageBox.StandardButton.Yes -> выполнить запрос DELETE FROM agents
        # TODO: Сохранить изменения и обновить таблицу
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgentsManager()
    window.show()
    sys.exit(app.exec())