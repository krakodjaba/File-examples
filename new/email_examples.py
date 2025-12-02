"""
email_examples.py

Расширенные примеры работы с EML-файлами в OSINT:

Key Features:
1. Парсинг заголовков и метаданных
2. Извлечение вложений и текста
3. Проверка репутации отправителя через API
4. Анализ временных меток
5. Выявление аномалий в заголовках

Типичные кейсы:
- Исследование фишинговых писем
- Отслеживание цепочек переписки
- Верификация отправителей
- Анализ подозрительных вложений
"""

import email
from email.header import decode_header
import os
import requests
from datetime import datetime
import hashlib

def parse_eml(filepath):
    """Загрузка и парсинг EML-файла."""
    with open(filepath, 'rb') as f:
        return email.message_from_binary_file(f)

def extract_headers(eml):
    """Извлечение и декодирование заголовков."""
    headers = {}
    for key, value in eml.items():
        decoded = decode_header(value)
        headers[key] = ''.join(
            [t[0].decode(t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0] 
             for t in decoded]
        )
    return headers

def save_attachments(eml, output_dir):
    """Сохранение вложений в указанную директорию."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    attachments = []
    for part in eml.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            if filename:
                file_path = f"{output_dir}/{filename}"
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                
                # Хеширование файла для анализа
                with open(file_path, 'rb') as f:
                    content = f.read()
                    sha256 = hashlib.sha256(content).hexdigest()
                    attachments.append({"filename": filename, "sha256": sha256})
    return attachments

def check_sender_reputation(email_address, api_key):
    """Проверка репутации отправителя через API (например, Hunter.io)."""
    url = f"https://api.hunter.io/v2/email-verifier?email={email_address}&api_key={api_key}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def analyze_timestamps(eml):
    """Анализ временных меток письма."""
    headers = extract_headers(eml)
    timestamps = {}
    for key in ['Date', 'Received']:
        if key in headers:
            try:
                timestamps[key] = datetime.strptime(headers[key], '%a, %d %b %Y %H:%M:%S %z')
            except:
                timestamps[key] = headers[key]
    return timestamps

def detect_suspicious_headers(eml):
    """Выявление подозрительных заголовков (например, подделка From)."""
    headers = extract_headers(eml)
    suspicious = []
    
    # Проверка несоответствия From и Return-Path
    if 'From' in headers and 'Return-Path' in headers:
        if not headers['From'].endswith(headers['Return-Path'].split('@')[-1]):
            suspicious.append("Несоответствие From и Return-Path")
    
    return suspicious

if __name__ == "__main__":
    # Тестовые данные
    TEST_EML = """From: sender@example.com
To: recipient@example.com
Subject: Test Email
Date: Mon, 01 Jan 2023 12:00:00 +0000
Content-Type: multipart/mixed; boundary="boundary"

--boundary
Content-Type: text/plain

This is a test email.

--boundary
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="test.txt"

Test attachment content.
--boundary--
"""
    with open("test_email.eml", 'w') as f:
        f.write(TEST_EML)
    
    # Демонстрация
    eml = parse_eml("test_email.eml")
    print("Заголовки:", extract_headers(eml))
    print("Вложения:", save_attachments(eml, "attachments"))
    print("Временные метки:", analyze_timestamps(eml))
    print("Подозрительные заголовки:", detect_suspicious_headers(eml))