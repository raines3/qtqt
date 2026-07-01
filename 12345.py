import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QInputDialog
from PyQt6 import uic

class BioTechApp(QMainWindow):
    def __init__(self, user_role):
        super().__init__()
        uic.loadUi("biotech.ui", self)
        self.db_name = "biotech.db"
        self.current_role = user_role

        self.init_medical_db()
        
        if self.current_role == "Главврач":
            self.admin_panel_box.setVisible(True)
            self.statusBar().showMessage("Доступ: Администатор (Главврач)")
        else:
            self.admin_panel_box.setVisible(False)
            self.statusBar().showMessage("Доступ: Ограниченый (Дежурный врач)")

        self.save_price_btn.clicked.connect(self.update_appointments_price)

        self.load_patients_to_combo()
        self.refresh_appointments_table()

    def init_medical_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS patients (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       diagnosis TEXT NOT NULL)""")
        
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS appointments (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       doctor_notes TEXT NOT NULL,
                       price INTEGER NOT NULL,
                       patient_id INTEGER NOT NULL,
                       FOREIGN KEY (patient_id) REFERENCES patients(id))""")
        
        cursor.execute("SELECT COUNT(*) from patients")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO patients (name, diagnosis) VALUES ('Иванов И. И.', 'ОРви')")
            cursor.execute("INSERT INTO patients (name, diagnosis) VALUES ('Васильев И. И.', 'Пневмония')")

            cursor.execute("INSERT INTO appointments (doctor_notes, price, patient_id) VALUES ('Постельныйрежим',1500, 1)")
            cursor.execute("INSERT INTO appointments (doctor_notes, price, patient_id) VALUES ('Назначение антибиотики',3500, 2)")
        conn.commit()
        conn.close()
    
    def load_patients_to_combo(self):
        self.patient_combo.clear()
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM patients")
        for row in cursor.fetchall():
            self.patient_combo.addItem(row[1], row[0])
        conn.close()

    def refresh_appointments_table(self):
        self.appointments_table.setRowCount(0)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT appointments.id, patients.name, patients.diagnosis, appointments.doctor_notes, appointments.price
                    FROM appointments
                    JOIN patients ON appointments.patient_id = patients.id
                    ORDER BY appointments.id ASC""")
        rows = cursor.fetchall()
        for row_idx, row_data in enumerate(rows):
            self.appointments_table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.appointments_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        conn.close()

    def update_appointments_price(self):
        new_price_str = self.price_input.text().strip()
        patient_db_id = self.patient_combo.currentData()

        if not new_price_str:
            QMessageBox.warning(self, "Ошибка", "Укажите стоимость приема")
            return
        try:
            price_int = int(new_price_str)
            if price_int < 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть неотрецательным числом")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET price = ? WHERE patient_id = ?", (price_int, patient_db_id))
        conn.commit()
        conn.close()

        self.price_input.clear()
        QMessageBox.information(self, "Успешно", "Стоимость услуг успешно обновлена")
        self.refresh_appointments_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    roles = ["Врач", "Главврач"]
    role, ok = QInputDialog.getItem(None, "Авторизация BioTech", "Выберете вашу должность: ", roles, 0, False)

    if ok and role:
        window = BioTechApp(role)
        window.show()
        sys.exit(app.exec())

    else:
        sys.exit(0)


        
    

            
        