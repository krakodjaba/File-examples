"""
yaml_examples.py

Расширенные примеры работы с YAML-файлами в OSINT:

Key Features:
1. Чтение, запись, парсинг YAML
2. Валидация схем (JSON Schema)
3. Извлечение данных по ключам
4. Конвертация в JSON/CSV
5. Анализ конфигов инструментов (Maltego, SpiderFoot)

Типичные кейсы:
- Парсинг конфигурационных файлов
- Валидация YAML-схем
- Извлечение параметров инструментов
"""

import yaml
import json
import pandas as pd
from jsonschema import validate, ValidationError

def read_yaml(filepath):
    """Чтение YAML-файла."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def write_yaml(data, filepath):
    """Запись YAML-файла."""
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def filter_yaml_by_key(filepath, key, value):
    """Фильтрация YAML по ключу и значению."""
    data = read_yaml(filepath)
    return [item for item in data.get('items', []) if item.get(key) == value]

def yaml_to_json(yaml_filepath, json_filepath):
    """Конвертация YAML в JSON."""
    data = read_yaml(yaml_filepath)
    with open(json_filepath, 'w') as f:
        json.dump(data, f, indent=4)

def yaml_to_csv(yaml_filepath, csv_filepath):
    """Конвертация YAML в CSV."""
    data = read_yaml(yaml_filepath)['items']
    pd.DataFrame(data).to_csv(csv_filepath, index=False)

def validate_yaml_schema(yaml_filepath, schema_filepath):
    """Валидация YAML по JSON Schema."""
    with open(yaml_filepath, 'r') as f:
        data = yaml.safe_load(f)
    
    with open(schema_filepath, 'r') as f:
        schema = json.load(f)
    
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
        return False

def parse_maltego_config(config_path):
    """Парсинг конфига Maltego."""
    config = read_yaml(config_path)
    transforms = config.get('transforms', [])
    return transforms

if __name__ == "__main__":
    # Тестовые данные
    TEST_YAML = """
    items:
      - name: Alice
        age: 30
        country: USA
      - name: Bob
        age: 25
        country: UK
    """
    with open("test_data.yaml", 'w') as f:
        f.write(TEST_YAML)
    
    # Демонстрация
    print("Пользователи из USA:", filter_yaml_by_key("test_data.yaml", "country", "USA"))
    yaml_to_json("test_data.yaml", "test_data.json")
    yaml_to_csv("test_data.yaml", "test_data.csv")