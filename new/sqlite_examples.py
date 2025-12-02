"""
sqlite_examples.py

Расширенные примеры работы с SQLite-файлами в OSINT:

Key Features:
1. Чтение, запись, выполнение запросов
2. Экспорт данных в CSV/JSON
3. Анализ структуры БД
4. Поиск аномалий (подозрительные записи)
5. Интеграция с Pandas

Типичные кейсы:
- Анализ дампов баз данных
- Исследование логов приложений
- Поиск скрытых таблиц
"""

import sqlite3
import pandas as pd
import json
import os
from collections import Counter

def create_test_db():
    """Создание тестовой базы данных."""
    conn = sqlite3.connect("test_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER, country TEXT)")
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("Alice", 30, "USA"))
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("Bob", 25, "UK"))
    conn.commit()
    conn.close()

def query_sqlite(db_filepath, query):
    """Выполнение SQL-запроса."""
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def sqlite_to_csv(db_filepath, table_name, csv_filepath):
    """Экспорт таблицы SQLite в CSV."""
    conn = sqlite3.connect(db_filepath)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    df.to_csv(csv_filepath, index=False)
    conn.close()

def sqlite_to_json(db_filepath, table_name, json_filepath):
    """Экспорт таблицы SQLite в JSON."""
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    with open(json_filepath, 'w') as f:
        json.dump(data, f, indent=4)
    conn.close()

def analyze_db_structure(db_filepath):
    """Анализ структуры базы данных."""
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def find_anomalies(db_filepath, table_name, column):
    """Поиск аномалий в данных (например, пустые значения)."""
    conn = sqlite3.connect(db_filepath)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    anomalies = df[df[column].isnull()]
    conn.close()
    return anomalies

if __name__ == "__main__":
    # Создание тестовой базы данных
    create_test_db()
    
    # Демонстрация
    print("Таблицы в БД:", analyze_db_structure("test_data.db"))
    print("Все пользователи:", query_sqlite("test_data.db", "SELECT * FROM users"))
    sqlite_to_csv("test_data.db", "users", "users.csv")
    sqlite_to_json("test_data.db", "users", "users.json")
    print("Аномалии в возрасте:", find_anomalies("test_data.db", "users", "age"))