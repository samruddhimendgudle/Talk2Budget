# storage.py
import sqlite3
import os

DB_PATH = os.path.join("data", "expenses.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            item TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(exp):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO expenses (date, item, price) VALUES (?, ?, ?)',
                (exp['date'], exp['item'], exp['price']))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT date, item, price FROM expenses ORDER BY date DESC, id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows
