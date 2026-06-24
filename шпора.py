import sqlite3

# ========== 1. ПОДКЛЮЧЕНИЕ И КУРСОР ==========
conn = sqlite3.connect('database.db')  # файл БД
# conn = sqlite3.connect(':memory:')   # БД в RAM
cursor = conn.cursor()

# ========== 2. СОЗДАНИЕ ТАБЛИЦЫ ==========
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

# ========== 3. ВСТАВКА ДАННЫХ ==========
# Одна запись (безопасно через ?)
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 25))

# С именованными параметрами
cursor.execute("INSERT INTO users (name, age) VALUES (:name, :age)", 
               {'name': 'Bob', 'age': 30})

# Множественная вставка
users_data = [('Charlie', 22), ('Diana', 28)]
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_data)

conn.commit()  # сохранить изменения!

# ========== 4. ВЫБОРКА ДАННЫХ ==========
cursor.execute("SELECT * FROM users WHERE age > ?", (20,))

# Способы получения данных
all_rows = cursor.fetchall()      # [(1, 'Alice', 25), (2, 'Bob', 30), ...]
one_row = cursor.fetchone()        # (1, 'Alice', 25)
few_rows = cursor.fetchmany(2)     # первые 2 строки

# Или итерация по cursor
cursor.execute("SELECT * FROM users")
for row in cursor:
    print(row)

# ========== 5. ОБНОВЛЕНИЕ ==========
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, 'Alice'))
conn.commit()

# ========== 6. УДАЛЕНИЕ ==========
cursor.execute("DELETE FROM users WHERE name = ?", ('Bob',))
conn.commit()

# ========== 7. ПОЛУЧЕНИЕ МЕТАДАННЫХ ==========
cursor.execute("SELECT * FROM users")
print("Последний ID:", cursor.lastrowid)   # для INSERT
print("Затронуто строк:", cursor.rowcount) # количество измененных/выбранных строк

# ========== 8. КОНТЕКСТНЫЙ МЕНЕДЖЕР (АВТО-COMMIT) ==========
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    # commit автоматический при выходе из with

# ========== 9. ПРИМЕР ГОТОВОЙ ФУНКЦИИ ==========
def get_users_by_age(min_age):
    """Вернуть список пользователей старше min_age"""
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, age FROM users WHERE age > ?", (min_age,))
        return cursor.fetchall()

# Использование
# users = get_users_by_age(25)
# print(users)

# ========== 10. ЗАКРЫТИЕ СОЕДИНЕНИЯ ==========
conn.close()

# ========== БЫСТРЫЕ ПРИМЕРЫ (РАСКОММЕНТИРУЙ ДЛЯ ТЕСТА) ==========
# Вставка и получение ID
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Eve', 35))
print("ID новой записи:", cursor.lastrowid)

# Проверка существования записи
cursor.execute("SELECT 1 FROM users WHERE name = ?", ('Alice',))
exists = cursor.fetchone() is not None
print("Alice exists:", exists)

# Получение одной колонкой (например, все имена)
cursor.execute("SELECT name FROM users")
names = [row[0] for row in cursor.fetchall()]
print("All names:", names)
