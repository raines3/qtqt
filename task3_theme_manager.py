# task3_theme_manager.py
# Практическая работа: Динамическое управление стилями приложения (Кастомная дизайн-система)
# 
# УСЛОВИЕ ЗАДАЧИ:
# Разработайте текстовый блокнот. На главном экране находится редактор текста, а вызов 
# дополнительного окна позволяет переключать тему оформления всего приложения (Светлая, Тёмная, Киберпанк).
#
# Спецификация интерфейса (Qt Designer):
# 1. Главное окно (main_pad.ui на базе QMainWindow):
#    - Многострочное текстовое поле QTextEdit для ввода заметок (objectName: text_editor).
#    - Кнопка QPushButton для открытия настроек внешнего вида (objectName: btn_theme).
# 2. Диалоговое окно (theme_dialog.ui на базе QDialog):
#    - Элемент списка QListWidget (objectName: list_themes), содержащий фиксированные строки: 
#      "Светлая тема", "Тёмная тема", "Тема Киберпанк". (Заполняется в дизайнере).
#    - Стандартные кнопки QDialogButtonBox (accept/reject).
#
# Регламент фиксации этапов разработки в Git:
# - Шаг 1: Разметка текстового редактора и списка тем. Коммит -> layout: сверстаны окна кастомной дизайн-системы
# - Шаг 2: Реализация глобального QSS-стилирования. Коммит -> feat: внедрено динамическое переключение тем оформления приложения

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

class ThemeDialog(QDialog):
    def __init__(self, parent=None):
        """
        Конструктор окна выбора темы. Загружает 'theme_dialog.ui'.
        """
        super().__init__(parent)
        uic.loadUi("theme_dialog.ui", self)
        # TODO: Загрузите файл разметки theme_dialog.ui
        

    def get_selected_theme_index(self):
        """
        Возвращает индекс выбранной строки из списка тем, чтобы определить выбор пользователя.
        
        :return: int -> Индекс выбранной строки (0, 1 или 2). Если ничего не выбрано, вернуть -1.
        """
        return self.list_themes.currentRow()
        # TODO: Считайте текущий индекс выбранной строки из list_themes
        # Подсказка: return self.list_themes.currentRow()

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Конструктор главного окна блокнота. Загружает 'main_pad.ui'.
        """
        super().__init__()
        # TODO: Загрузите файл разметки main_pad.ui
        # TODO: Назначьте метод change_theme обработчиком клика по кнопке btn_theme
        uic.loadUi("main_pad.ui", self)
        self.btn_theme.clicked.connect(self.change_theme)

    def change_theme(self):
        """
        Вызывает модальное окно тем. В зависимости от выбранного индекса, применяет 
        глобальный стиль ко всему приложению через метод приложения self.setStyleSheet().
        """
        # TODO: Откройте ThemeDialog модально
        # TODO: Если диалог подтвержден, получите выбранный индекс. 
        # Подсказка по стилям QSS:
        # Индекс 0 (Светлая): "background-color: #ffffff; color: #000000;"
        # Индекс 1 (Тёмная): "background-color: #2b2b2b; color: #ffffff;"
        # Индекс 2 (Киберпанк): "background-color: #000000; color: #00ff00; font-family: monospace;"
        # Применить стиль ко всему окну: self.setStyleSheet(qss_string)
        dialog = ThemeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            idx = dialog.get_selected_theme_index()
            print(idx)
            
            if idx == -1:
                self.setStyleSheet("background-color: #ffffff; color: #000000;")
            elif idx == 1:
                self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
            elif idx == 2:
                self.setStyleSheet("background-color: #000000; color: #00ff00; font-family: monospace;")
            




        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())