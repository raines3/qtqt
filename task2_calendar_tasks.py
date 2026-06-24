# task2_calendar_tasks.py
# Практическая работа: Интеграция сложных виджетов (Менеджер задач с календарем дедлайнов)
# 
# УСЛОВИЕ ЗАДАЧИ:
# Создайте планировщик задач, где в главном окне находится список текущих дел, а форма 
# добавления новой задачи включает в себя интерактивный календарь для выбора даты дедлайна.
#
# Спецификация интерфейса (Qt Designer):
# 1. Главное окно (main_todo.ui на базе QMainWindow):
#    - Элемент QListWidget для вывода списка задач (objectName: list_tasks).
#    - Кнопка QPushButton для создания новой записи (objectName: btn_new_task).
# 2. Диалоговое окно (task_dialog.ui на базе QDialog):
#    - Текстовое поле QLineEdit для формулировки сути задачи (objectName: input_task_name).
#    - Виджет календаря QCalendarWidget для указания даты (objectName: calendar_deadline).
#    - Кнопки QDialogButtonBox, настроенные в режиме сигналов/слотов (F4) на accept/reject.
#
# Регламент фиксации этапов разработки в Git:
# - Шаг 1: Интеграция виджета календаря. Коммит -> layout: подготовлена форма планировщика с QCalendarWidget
# - Шаг 2: Парсинг дат и наполнение списка. Коммит -> feat: реализован перенос задач с форматированием даты дедлайна

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

class TaskDialog(QDialog):
    def __init__(self, parent=None):
        """
        Конструктор диалога. Загружает 'task_dialog.ui'.
        """
        super().__init__(parent)
        uic.loadUi("task_dialog.ui", self)
    

        # TODO: Загрузите файл разметки task_dialog.ui
        

    def get_task_data(self):
        """
        Извлекает текст задачи и выбранную в календаре дату.
        Для работы с датой извлеките объект QDate и переведите его в строку.
        
        :return: (str, str) -> (Текст задачи, Дата дедлайна в формате строки)
        """
        task_text = self.input_task_name.text()
        date_object = self.calendar_deadline.selectedDate()
        date_str = date_object.toString("dd.MM.yyyy")

        # TODO: Считайте текст из input_task_name.
        # TODO: Извлеките дату из календаря. 
        # Подсказка: date_object = self.calendar_deadline.selectedDate()
        #            date_str = date_object.toString("dd.MM.yyyy")
        return str(task_text), date_str

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Конструктор главного окна планировщика. Загружает 'main_todo.ui'.
        """
        super().__init__()
        uic.loadUi("main_todo.ui", self)

        # TODO: Загрузите файл разметки main_todo.ui
        # TODO: Свяжите нажатие кнопки btn_new_task с методом create_task

        self.btn_new_task.clicked.connect(self.create_task)
        

    def create_task(self):
        """
        Открывает диалог создания задачи. При успешном сохранении формирует запись
        в формате: "[📅 Дата] - Текст задачи" и добавляет её в list_tasks.
        """
        # TODO: Вызовите TaskDialog модально
        # TODO: В случае успеха сформируйте строку и внесите её новой записью в self.list_tasks
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task, date = dialog.get_task_data()

            self.list_tasks.addItem(f"Задача: {task} - Дата: {date}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())