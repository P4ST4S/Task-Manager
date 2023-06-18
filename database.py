import sqlite3


def create_database():
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    due_date TEXT NOT NULL,
    priority INTEGER NOT NULL,
    status TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()


def connect_db():
    conn = sqlite3.connect('task_manager.db')
    return conn
