"""
blockchain_examples.py

Расширенные примеры работы с блокчейн-данными в OSINT:

Key Features:
1. Парсинг JSON-дампов транзакций (Bitcoin/Ethereum)
2. Построение графа связей между адресами
3. Анализ объёмов транзакций
4. Экспорт в GraphML для Gephi

Типичные кейсы:
- Отслеживание перемещения средств
- Выявление связей между кошельками
- Визуализация сложных транзакционных цепочек
"""

import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def parse_transactions(json_file):
    """Парсинг транзакций из JSON."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data.get("transactions", [])

def analyze_addresses(transactions):
    """Анализ уникальных адресов."""
    addresses = set()
    for tx in transactions:
        addresses.update(tx.get("inputs", []))
        addresses.update(tx.get("outputs", []))
    return list(addresses)

def calculate_transaction_volume(transactions):
    """Расчёт общего объёма транзакций."""
    return sum(tx.get('value', 0) for tx in transactions)

def find_high_value_transactions(transactions, threshold):
    """Поиск транзакций с суммой выше порога."""
    return [tx for tx in transactions if tx.get('value', 0) > threshold]

def export_to_graphml(transactions, output_file):
    """Экспорт графа в GraphML для анализа в Gephi."""
    G = nx.Graph()
    for tx in transactions:
        G.add_edges_from((inp, out) for inp in tx.get('inputs', []) 
                         for out in tx.get('outputs', []))
    nx.write_graphml(G, output_file)

def plot_transaction_graph(transactions):
    """Улучшенная визуализация графа транзакций."""
    G = nx.Graph()
    for tx in transactions:
        for inp in tx.get('inputs', []):
            for out in tx.get('outputs', []):
                G.add_edge(inp, out, weight=tx.get('value', 0.1))
    
    pos = nx.spring_layout(G, k=0.5)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Transaction Graph", size=15)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('transaction_graph.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    # Тестовые данные
    TEST_DATA = {
        "transactions": [
            {
                "txid": "a1b2c3", 
                "inputs": ["wallet_A", "wallet_B"],
                "outputs": ["wallet_C", "wallet_D"],
                "value": 1.5,
                "timestamp": "2023-01-01"
            },
            {
                "txid": "d4e5f6",
                "inputs": ["wallet_C"],
                "outputs": ["wallet_E", "wallet_F"],
                "value": 0.8,
                "timestamp": "2023-01-02"
            }
        ]
    }
    
    # Сохранение тестовых данных
    with open('blockchain_data.json', 'w') as f:
        json.dump(TEST_DATA, f, indent=2)
    
    # Демонстрация
    transactions = parse_transactions('blockchain_data.json')
    print("Уникальные адреса:", analyze_addresses(transactions))
    print("Общий объём:", calculate_transaction_volume(transactions), "BTC")
    export_to_graphml(transactions, 'transactions.graphml')
    plot_transaction_graph(transactions)