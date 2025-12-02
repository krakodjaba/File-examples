"""
json_examples.py

Примеры работы с JSON-файлами в OSINT:
- Чтение, запись, фильтрация.
- Конвертация в другие форматы (CSV, Excel).
- Анализ данных (частотность значений).
"""

import json
import pandas as pd
from collections import Counter

# Тестовые данные
TEST_JSON_DATA = [
    {"name": "Alice", "age": 30, "country": "USA"},
    {"name": "Bob", "age": 25, "country": "UK"},
    {"name": "Charlie", "age": 35, "country": "Canada"},
]

def read_json(filepath):
    """Чтение JSON-файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data, filepath):
    """Запись данных в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def filter_json_by_key(filepath, key, value):
    """Фильтрация JSON по ключу и значению."""
    data = read_json(filepath)
    return [item for item in data if item.get(key) == value]

def json_to_dataframe(filepath):
    """Конвертация JSON в DataFrame."""
    return pd.read_json(filepath)

def analyze_json_values(filepath, key):
    """Анализ значений по ключу (например, частота стран)."""
    data = read_json(filepath)
    values = [item[key] for item in data if key in item]
    return Counter(values)

def json_to_csv(json_filepath, csv_filepath):
    """Экспорт JSON в CSV."""
    df = json_to_dataframe(json_filepath)
    df.to_csv(csv_filepath, index=False)

def json_to_excel(json_filepath, excel_filepath):
    """Экспорт JSON в Excel."""
    df = json_to_dataframe(json_filepath)
    df.to_excel(excel_filepath, index=False)

if __name__ == "__main__":
    # Примеры использования
    write_json(TEST_JSON_DATA, "test_data.json")
    print("Прочитанные данные:", read_json("test_data.json"))
    print("Фильтрация по стране (USA):", filter_json_by_key("test_data.json", "country", "USA"))
    print("Анализ стран:", analyze_json_values("test_data.json", "country"))
    json_to_csv("test_data.json", "test_data.csv")
    json_to_excel("test_data.json", "test_data.xlsx")