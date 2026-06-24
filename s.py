import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt

class MusicTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("music.ui", self)
        self.db_name =  'music.db'
        self.init_db()
        self.add_btn.clicked.connect(self.add_track)
        self.filter_btn.clicked.connect(self.toogle_filter)
        self.filter_active = False
        self.refresh_table()


    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute(""" 
                CREATE TABLE IF NOT EXISTS tracks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    rating INTEGER NOT NULL)
                                  """)
    def refresh_table(self, filter_stars=None):
        self.music_table.setRowCount(0)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if filter_stars:
                cursor.execute("SELECT * FROM tracks WHERE rating = ?", (filter_stars,))
            else:
                cursor.execute("SELECT * FROM tracks")
        
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.music_table.insertRow(row_idx)
            for col_idx, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                if col_idx in (0, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.music_table.setItem(row_idx, col_idx, item)

    def add_track(self):
        title = self.title_input.text().strip()
        artist = self.artist_input.text().strip()
        rating = self.rating_input.text().strip()
        if not title or not artist or not rating.isdigit() or not (1 <=int(rating) <= 5):
            QMessageBox.warning(self,"Ошибка", "Заполните все поля! Рейтинг от 1 до 5")
            return
        with sqlite3.connect(self.db_name) as conn:
            conn.cursor().execute(
                "INSERT INTO tracks (title,artist,rating) VALUES (?,?,?)", (title, artist, int(rating))
            )
        
        self.title_input.clear()
        self.artist_input.clear()
        self.rating_input.clear()
        self.refresh_table()

    def toogle_filter(self):
        if not self.filter_active:
            self.filter_active = True
            self.filter_btn.setText("Показать всё")
            self.refresh_table(filter_stars=5)
        else:
            self.filter_active = False
            self.filter_btn.setText("Шедевры")
            self.refresh_table()
            



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicTrackerApp()
    window.show()
    sys.exit(app.exec())

