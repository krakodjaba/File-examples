"""
log_examples.py

Расширенные примеры работы с лог-файлами в OSINT:

Key Features:
1. Парсинг логов Nginx/Apache
2. Фильтрация по IP, дате, статусу
3. Анализ трафика
4. Выявление аномалий (например, подозрительные IP)
5. Экспорт данных в CSV/JSON

Типичные кейсы:
- Анализ веб-серверов
- Поиск атак (DDoS, сканирование)
- Мониторинг подозрительной активности
"""

import re
from collections import Counter
import pandas as pd
import json

def parse_log_line(line):
    """Парсинг одной строки лога (Nginx/Apache)."""
    pattern = r'(\d+\.\d+\.\d+\.\d+) .* \[(.*?)\] "(.*?)" (\d+) (\d+)'
    match = re.match(pattern, line)
    if match:
        return {
            'ip': match.group(1),
            'time': match.group(2),
            'request': match.group(3),
            'status': match.group(4),
            'bytes': match.group(5)
        }
    return None

def filter_logs_by_ip(filepath, ip):
    """Фильтрация логов по IP."""
    with open(filepath, 'r') as f:
        return [line for line in f if ip in line]

def count_status_codes(filepath):
    """Подсчёт статус-кодов."""
    with open(filepath, 'r') as f:
        statuses = [parse_log_line(line)['status'] for line in f if parse_log_line(line)]
        return Counter(statuses)

def detect_suspicious_ips(filepath, threshold=100):
    """Выявление подозрительных IP (например, слишком много запросов)."""
    with open(filepath, 'r') as f:
        ips = [parse_log_line(line)['ip'] for line in f if parse_log_line(line)]
        ip_counts = Counter(ips)
        return [ip for ip, count in ip_counts.items() if count > threshold]

def logs_to_dataframe(filepath):
    """Конвертация логов в DataFrame."""
    with open(filepath, 'r') as f:
        data = [parse_log_line(line) for line in f if parse_log_line(line)]
    return pd.DataFrame(data)

def export_logs_to_json(filepath, output_file):
    """Экспорт логов в JSON."""
    df = logs_to_dataframe(filepath)
    df.to_json(output_file, orient='records', indent=4)

if __name__ == "__main__":
    # Тестовые данные
    TEST_LOG = """127.0.0.1 - - [01/Jan/2023:00:00:01 +0000] "GET / HTTP/1.1" 200 1234
192.168.1.1 - - [01/Jan/2023:00:00:02 +0000] "POST /login HTTP/1.1" 403 567
10.0.0.1 - - [01/Jan/2023:00:00:03 +0000] "GET /admin HTTP/1.1" 404 0"""
    
    with open("test_data.log", 'w') as f:
        f.write(TEST_LOG)
    
    # Демонстрация
    print("Статус-коды:", count_status_codes("test_data.log"))
    print("Подозрительные IP:", detect_suspicious_ips("test_data.log", threshold=1))
    df = logs_to_dataframe("test_data.log")
    print(df.head())
    export_logs_to_json("test_data.log", "logs.json")