"""
csv_examples.py

Примеры работы с CSV/TSV-файлами в OSINT:
- Чтение, запись, фильтрация.
- Конвертация в JSON, Excel.
- Анализ данных (уникальные значения, объединение файлов).
"""

import pandas as pd

# Тестовые данные
TEST_CSV_DATA = "name,age,country\nAlice,30,USA\nBob,25,UK\nCharlie,35,Canada"

def read_csv(filepath, delimiter=','):
    """Чтение CSV/TSV-файла."""
    return pd.read_csv(filepath, delimiter=delimiter)

def write_csv(data, filepath, delimiter=','):
    """Запись данных в CSV/TSV."""
    data.to_csv(filepath, sep=delimiter, index=False)

def filter_csv_by_column(filepath, column, value):
    """Фильтрация CSV по значению столбца."""
    df = read_csv(filepath)
    return df[df[column] == value]

def csv_to_json(csv_filepath, json_filepath):
    """Конвертация CSV в JSON."""
    df = read_csv(csv_filepath)
    df.to_json(json_filepath, orient='records', indent=4)

def analyze_csv_column(filepath, column):
    """Анализ столбца (например, уникальные значения)."""
    df = read_csv(filepath)
    return df[column].value_counts()

if __name__ == "__main__":
    # Примеры использования
    with open("test_data.csv", 'w', encoding='utf-8') as f:
        f.write(TEST_CSV_DATA)
    print("Фильтрация по стране (USA):", filter_csv_by_column("test_data.csv", "country", "USA"))
    print("Анализ возраста:", analyze_csv_column("test_data.csv", "age"))
    csv_to_json("test_data.csv", "test_data.json")