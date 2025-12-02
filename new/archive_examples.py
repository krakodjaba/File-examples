"""
archive_examples.py

Расширенные примеры работы с архивами в OSINT:

Key Features:
1. Извлечение файлов из ZIP/TAR
2. Поиск по содержимому
3. Анализ метаданных архива
4. Выявление подозрительных файлов (например, исполняемые)
5. Экспорт данных в CSV/JSON

Типичные кейсы:
- Анализ архивов с утечками данных
- Поиск в логах и конфигах
- Выявление вредоносных файлов
"""

import zipfile
import tarfile
import pandas as pd
import os
import re

def list_archive_files(archive_path):
    """Список файлов в архиве."""
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            return z.namelist()
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as t:
            return t.getnames()

def extract_file_from_archive(archive_path, filename, output_path):
    """Извлечение файла из архива."""
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extract(filename, output_path)
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as t:
            t.extract(filename, output_path)

def search_in_archive(archive_path, pattern):
    """Поиск по содержимому архива."""
    results = []
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            for name in z.namelist():
                with z.open(name) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    if re.search(pattern, content, re.IGNORECASE):
                        results.append(name)
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as t:
            for member in t.getmembers():
                if member.isfile():
                    with t.extractfile(member) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        if re.search(pattern, content, re.IGNORECASE):
                            results.append(member.name)
    return results

def analyze_archive_metadata(archive_path):
    """Анализ метаданных архива (размеры, даты)."""
    metadata = []
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            for info in z.infolist():
                metadata.append({
                    'filename': info.filename,
                    'size': info.file_size,
                    'modified': info.date_time
                })
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as t:
            for member in t.getmembers():
                metadata.append({
                    'filename': member.name,
                    'size': member.size,
                    'modified': member.mtime
                })
    return metadata

def detect_executable_files(archive_path):
    """Выявление исполняемых файлов в архиве."""
    executables = []
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            for name in z.namelist():
                if name.endswith(('.exe', '.bat', '.sh', '.ps1')):
                    executables.append(name)
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as t:
            for member in t.getmembers():
                if member.name.endswith(('.sh', '.py', '.pl')):
                    executables.append(member.name)
    return executables

def export_archive_data_to_csv(archive_path, output_file):
    """Экспорт метаданных архива в CSV."""
    metadata = analyze_archive_metadata(archive_path)
    df = pd.DataFrame(metadata)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Тестовые данные (создаем ZIP-архив)
    with zipfile.ZipFile("test_data.zip", 'w') as z:
        z.writestr("file1.txt", "This is file 1 with OSINT data")
        z.writestr("file2.csv", "name,age\nAlice,30")
        z.writestr("script.sh", "#!/bin/bash\necho 'OSINT script'")
    
    # Демонстрация
    print("Файлы в архиве:", list_archive_files("test_data.zip"))
    print("Поиск 'OSINT':", search_in_archive("test_data.zip", "OSINT"))
    print("Исполняемые файлы:", detect_executable_files("test_data.zip"))
    export_archive_data_to_csv("test_data.zip", "archive_metadata.csv")
    print("Метаданные экспортированы в archive_metadata.csv")