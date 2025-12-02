"""
excel_examples.py

Примеры работы с Excel-файлами в OSINT:
- Чтение, запись, фильтрация.
- Конвертация в CSV, JSON.
- Анализ данных (статистика по столбцам).
"""

import pandas as pd

# Тестовые данные
TEST_EXCEL_DATA = {"name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35], "country": ["USA", "UK", "Canada"]}

def read_excel(filepath, sheet_name=0):
    """Чтение Excel-файла."""
    return pd.read_excel(filepath, sheet_name=sheet_name)

def write_excel(data, filepath, sheet_name='Sheet1'):
    """Запись данных в Excel."""
    data.to_excel(filepath, sheet_name=sheet_name, index=False)

def excel_to_csv(excel_filepath, csv_filepath, sheet_name=0):
    """Конвертация Excel в CSV."""
    df = read_excel(excel_filepath, sheet_name)
    df.to_csv(csv_filepath, index=False)

def analyze_excel_column(filepath, column, sheet_name=0):
    """Анализ столбца (например, среднее значение)."""
    df = read_excel(filepath, sheet_name)
    return df[column].describe()

if __name__ == "__main__":
    # Примеры использования
    df = pd.DataFrame(TEST_EXCEL_DATA)
    write_excel(df, "test_data.xlsx")
    print("Анализ возраста:", analyze_excel_column("test_data.xlsx", "age"))
    excel_to_csv("test_data.xlsx", "test_data.csv")