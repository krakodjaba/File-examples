"""
xml_examples.py

Расширенные примеры работы с XML-файлами в OSINT:

Key Features:
1. Чтение, запись, парсинг XML
2. Извлечение данных по тегам и XPath
3. Валидация схем (XSD)
4. Конвертация в JSON/CSV
5. Поиск аномалий в структуре

Типичные кейсы:
- Анализ RSS-лент и новостных потоков
- Парсинг конфигурационных файлов
- Валидация XML-данных
"""

import xml.etree.ElementTree as ET
import json
import pandas as pd

def read_xml(filepath):
    """Чтение XML-файла."""
    return ET.parse(filepath)

def write_xml(root, filepath):
    """Запись XML-файла."""
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)

def extract_xml_tags(filepath, tag):
    """Извлечение данных по тегу."""
    tree = read_xml(filepath)
    return [elem.text for elem in tree.findall(f'.//{tag}')]

def xml_to_json(xml_filepath, json_filepath):
    """Конвертация XML в JSON."""
    tree = read_xml(xml_filepath)
    data = []
    for user in tree.findall('.//user'):
        data.append({
            'name': user.find('name').text,
            'age': int(user.find('age').text),
            'country': user.find('country').text
        })
    with open(json_filepath, 'w') as f:
        json.dump(data, f, indent=4)

def xml_to_csv(xml_filepath, csv_filepath):
    """Конвертация XML в CSV."""
    tree = read_xml(xml_filepath)
    data = []
    for user in tree.findall('.//user'):
        data.append({
            'name': user.find('name').text,
            'age': user.find('age').text,
            'country': user.find('country').text
        })
    pd.DataFrame(data).to_csv(csv_filepath, index=False)

def validate_xml_schema(xml_filepath, xsd_filepath):
    """Валидация XML по XSD-схеме (требуется lxml)."""
    try:
        from lxml import etree
        with open(xsd_filepath, 'r') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
        
        with open(xml_filepath, 'r') as f:
            xml_doc = etree.parse(f)
        
        return schema.validate(xml_doc)
    except ImportError:
        print("Установите lxml: pip install lxml")
        return False

def find_anomalies_in_xml(filepath):
    """Поиск аномалий в структуре XML (например, отсутствующие теги)."""
    tree = read_xml(filepath)
    issues = []
    
    for user in tree.findall('.//user'):
        if user.find('name') is None:
            issues.append(f"Нет тега 'name' в user {user}")
        if user.find('age') is None:
            issues.append(f"Нет тега 'age' в user {user}")
    
    return issues

if __name__ == "__main__":
    # Тестовые данные
    TEST_XML = """<?xml version="1.0"?>
    <users>
        <user>
            <name>Alice</name>
            <age>30</age>
            <country>USA</country>
        </user>
        <user>
            <name>Bob</name>
            <age>25</age>
            <country>UK</country>
        </user>
    </users>"""
    
    with open("test_data.xml", 'w') as f:
        f.write(TEST_XML)
    
    # Демонстрация
    print("Имена:", extract_xml_tags("test_data.xml", "name"))
    xml_to_json("test_data.xml", "test_data.json")
    xml_to_csv("test_data.xml", "test_data.csv")
    print("Аномалии:", find_anomalies_in_xml("test_data.xml"))