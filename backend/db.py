import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        credits INTEGER DEFAULT 3,
        premium INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()
