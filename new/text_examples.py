"""
text_examples.py

Примеры работы с текстовыми файлами в OSINT:
- Чтение, запись, поиск, замена.
- Анализ текста (подсчёт слов, email-адресов).
- Конвертация в табличные форматы.
"""

import re
from collections import Counter
import pandas as pd

# Тестовые данные
TEST_TEXT = """
Alice,30,USA
Bob,25,UK
Charlie,35,Canada
"""

def read_text(filepath):
    """Чтение текстового файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_text(content, filepath):
    """Запись текста в файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def search_in_text(filepath, pattern):
    """Поиск по регулярному выражению."""
    text = read_text(filepath)
    return re.findall(pattern, text)

def count_words(filepath):
    """Подсчёт слов в файле."""
    text = read_text(filepath)
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def text_to_dataframe(filepath, delimiter=','):
    """Конвертация текста в DataFrame."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip().split(delimiter) for line in f]
    return pd.DataFrame(lines)

def extract_emails(filepath):
    """Извлечение email-адресов из текста."""
    text = read_text(filepath)
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

def replace_in_text(filepath, old_str, new_str):
    """Замена подстроки в тексте."""
    text = read_text(filepath)
    new_text = text.replace(old_str, new_str)
    write_text(new_text, filepath)

if __name__ == "__main__":
    # Примеры использования
    write_text(TEST_TEXT, "test_data.txt")
    print("Поиск чисел:", search_in_text("test_data.txt", r'\d+'))
    print("Подсчёт слов:", count_words("test_data.txt"))
    print("Конвертация в DataFrame:", text_to_dataframe("test_data.txt"))