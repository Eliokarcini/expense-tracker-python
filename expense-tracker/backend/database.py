import sqlite3
import os
from datetime import datetime

def init_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data
    sample_expenses = [
        ('Groceries', 85.50, 'Food', '2024-01-15'),
        ('Movie Tickets', 25.00, 'Entertainment', '2024-01-14'),
        ('Gas', 45.75, 'Transportation', '2024-01-13'),
        ('Coffee', 4.50, 'Food', '2024-01-12'),
        ('Netflix', 15.99, 'Entertainment', '2024-01-10')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO expenses (description, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', sample_expenses)
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('expenses.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn