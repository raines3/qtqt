# task4_secure_notes.py
# Практическая работа: Проектирование систем контроля доступа (Секретные заметки с авторизацией)
# 
# УСЛОВИЕ ЗАДАЧИ:
# Напишите систему хранения конфиденциальной информации. При запуске главного окна текст 
# заметок заблокирован. Пользователь должен нажать кнопку «Авторизация», ввести пароль 
# в модальном окне, и в случае успеха получить доступ к редактированию.
#
# Спецификация интерфейса (Qt Designer):
# 1. Главное окно (main_secure.ui на базе QMainWindow):
#    - Поле QTextEdit для секретного текста (objectName: secure_editor). 
#      В свойствах изначально установить флаг readOnly в значение True (активировать блокировку).
#    - Кнопка QPushButton для входа (objectName: btn_login).
# 2. Диалоговое окно (login_dialog.ui на базе QDialog):
#    - Поле QLineEdit для ввода секретного ключа (objectName: input_password). 
#      * Важно: В свойствах виджета установите параметр echoMode в значение Password, 
#        чтобы вводимые символы скрывались звездочками.
#    - Кнопки QDialogButtonBox со стандартными сигналами закрытия окна.
#
# Регламент фиксации этапов разработки в Git:
# - Шаг 1: Разметка интерфейса безопасности. Коммит -> layout: развернуты защищенные компоненты интерфейса
# - Шаг 2: Валидация пароля и разблокировка виджетов. Коммит -> feat: реализована валидация ключа доступа в QDialog

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt6 import uic

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        """
        Конструктор окна авторизации. Загружает 'login_dialog.ui'.
        """
        super().__init__(parent)
        # TODO: Загрузите файл разметки login_dialog.ui
        uic.loadUi("login_dialog.ui", self)

    def get_password(self):
        """
        Возвращает введенный пользователем пароль.
        
        :return: str -> Строка пароля
        """
        # TODO: Верните текст из поля input_password

        return self.input_password.text()

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Конструктор защищенного приложения. Загружает 'main_secure.ui'.
        """
        super().__init__()
        uic.loadUi("main_secure.ui", self)
        # TODO: Загрузите файл разметки main_secure.ui
        # TODO: Привяжите кнопку btn_login к методу check_access
        self.btn_login.clicked.connect(self.check_access)

    def check_access(self):
        """
        Открывает окно ввода пароля. Сверяет пароль со строкой-эталоном (например, "admin123").
        При успехе снимает блокировку с текстового поля secure_editor и меняет текст кнопки.
        При ошибке выводит предупреждение через всплывающий виджет QMessageBox.
        """
        # TODO: Инициализируйте и запустите LoginDialog модально.
        # TODO: Если окно закрыто кнопкой ОК, проверьте пароль.
        #       Если пароль равен "admin123":
        #           self.secure_editor.setReadOnly(False)  # Снимаем блокировку
        #           self.btn_login.setEnabled(False)       # Отключаем кнопку входа
        #       Иначе:
        #           Вызовите предупреждение: QMessageBox.critical(self, "Ошибка", "Неверный ключ доступа!")
        dialog = LoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.get_password()
            if password == "admin123":
                self.secure_editor.setReadOnly(False)
                self.btn_login.setEnabled(False)
            else:
                QMessageBox.critical(self, "Ошибка", "Неверный ключ доступа!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())