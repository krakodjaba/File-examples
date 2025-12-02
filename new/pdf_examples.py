"""
pdf_examples.py

Расширенные примеры работы с PDF-файлами в OSINT:

Key Features:
1. Извлечение текста и метаданных
2. Анализ структуры документа
3. Поддержка OCR для отсканированных PDF
4. Экспорт данных в CSV/JSON

Типичные кейсы:
- Исследование документов на наличие скрытых метаданных
- Анализ отсканированных отчетов
- Парсинг таблиц из PDF
"""

import PyPDF2
from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image
import json
import pandas as pd
import os
from pdf2image import convert_from_path

def extract_pdf_text(filepath):
    """Извлечение текста из PDF (для текстовых PDF)."""
    try:
        return extract_text(filepath)
    except Exception as e:
        print(f"Ошибка извлечения текста: {e}")
        return None

def extract_pdf_metadata(filepath):
    """Извлечение метаданных PDF."""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return reader.metadata

def ocr_pdf_page(filepath, page_num=0, dpi=300):
    """OCR для отсканированных PDF (требуется pytesseract)."""
    try:
        images = convert_from_path(filepath, dpi=dpi, first_page=page_num+1, last_page=page_num+1)
        return pytesseract.image_to_string(images[0])
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return None

def analyze_pdf_structure(filepath):
    """Анализ структуры PDF (количество страниц, размеры)."""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return {
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "metadata": reader.metadata
        }

def export_pdf_data(filepath, output_format='csv'):
    """Экспорт данных PDF в CSV/JSON."""
    data = {
        "metadata": extract_pdf_metadata(filepath),
        "text_sample": extract_pdf_text(filepath)[:1000]  # Первые 1000 символов
    }
    
    if output_format == 'csv':
        pd.DataFrame([data]).to_csv("pdf_metadata.csv", index=False)
    else:
        with open("pdf_metadata.json", 'w') as f:
            json.dump(data, f, indent=4)

def search_in_pdf(filepath, keyword):
    """Поиск ключевого слова в PDF."""
    text = extract_pdf_text(filepath)
    return keyword in text if text else False

if __name__ == "__main__":
    # Пример использования
    pdf_path = "example.pdf"
    if not os.path.exists(pdf_path):
        print("Создайте example.pdf для тестирования")
    else:
        print("Метаданные:", extract_pdf_metadata(pdf_path))
        export_pdf_data(pdf_path, 'json')
        print("Найдено 'OSINT':", search_in_pdf(pdf_path, "OSINT"))