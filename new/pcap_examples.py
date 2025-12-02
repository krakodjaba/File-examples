"""
pcap_examples.py

Расширенные примеры работы с PCAP-файлами в OSINT:

Key Features:
1. Анализ сетевого трафика (IP, порты, протоколы)
2. Фильтрация пакетов по критериям
3. Экспорт данных в CSV для дальнейшего анализа
4. Интеграция с Wireshark/tshark

Типичные кейсы:
- Исследование сетевых атак
- Мониторинг подозрительной активности
- Анализ трафика приложений
"""

import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
import subprocess
import os

def read_pcap(filepath):
    """Чтение PCAP-файла с обработкой ошибок."""
    try:
        return rdpcap(filepath)
    except Exception as e:
        print(f"Ошибка чтения PCAP: {e}")
        return None

def extract_ips(pcap_file):
    """Извлечение уникальных IP-адресов."""
    packets = read_pcap(pcap_file)
    if not packets:
        return []
    
    ips = set()
    for pkt in packets:
        if IP in pkt:
            ips.update([pkt[IP].src, pkt[IP].dst])
    return list(ips)

def filter_by_protocol(pcap_file, protocol):
    """Фильтрация пакетов по протоколу (TCP/UDP)."""
    packets = read_pcap(pcap_file)
    if not packets:
        return []
    
    return [pkt for pkt in packets if protocol in pkt]

def export_to_csv(pcap_file, csv_file):
    """Экспорт метаданных трафика в CSV."""
    packets = read_pcap(pcap_file)
    if not packets:
        return
    
    data = []
    for pkt in packets:
        if IP in pkt:
            data.append({
                "src_ip": pkt[IP].src,
                "dst_ip": pkt[IP].dst,
                "protocol": pkt[IP].proto,
                "size": len(pkt)
            })
    pd.DataFrame(data).to_csv(csv_file, index=False)

def analyze_with_tshark(pcap_file):
    """Анализ PCAP через tshark (если установлен)."""
    if not os.path.exists(pcap_file):
        print("Файл не найден.")
        return
    
    try:
        result = subprocess.run(
            ["tshark", "-r", pcap_file, "-T", "fields", "-e", "ip.src", "-e", "ip.dst"],
            capture_output=True, text=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("Установите Wireshark/tshark для использования этой функции.")

if __name__ == "__main__":
    
    # Демонстрация
    print("Уникальные IP:", extract_ips("new/example.pcap"))
    export_to_csv("new/example.pcap", "pcap_analysis.csv")
    analyze_with_tshark("new/example.pcap")