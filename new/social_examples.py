"""
social_examples.py

Расширенные примеры работы с данными соцсетей в OSINT:

Key Features:
1. Парсинг JSON-дампов Twitter/Reddit
2. Анализ временных рядов активности
3. Визуализация графов взаимодействий
4. Экспорт данных в GEXF для Gephi
5. Интеграция с API (Twitter/Reddit)

Типичные кейсы:
- Исследование активности аккаунтов
- Анализ распространения информации
- Выявление координационных кампаний
"""

import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx

def load_social_data(filepath):
    """Загрузка JSON-дампов из файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f).get('posts', [])

def analyze_hashtags(posts):
    """Анализ хэштегов с частотностью."""
    hashtags = []
    for post in posts:
        if 'hashtags' in post:
            hashtags.extend(post['hashtags'])
    return Counter(hashtags)

def visualize_activity(posts):
    """Визуализация активности по времени."""
    timestamps = [post['timestamp'] for post in posts]
    df = pd.DataFrame({'timestamp': pd.to_datetime(timestamps)})
    df['hour'] = df['timestamp'].dt.hour
    activity = df['hour'].value_counts().sort_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(activity.index, activity.values, marker='o')
    plt.title('Активность по часам')
    plt.xlabel('Час')
    plt.ylabel('Количество постов')
    plt.grid()
    plt.savefig('activity.png')
    plt.show()

def detect_high_frequency_authors(posts, threshold=5):
    """Выявление авторов с подозрительно высокой активностью."""
    authors = Counter(p['author'] for p in posts)
    return [user for user, count in authors.items() if count > threshold]

def export_to_gexf(posts, output_file):
    """Экспорт графа взаимодействий в GEXF (для Gephi)."""
    G = nx.Graph()
    for post in posts:
        G.add_node(post['author'])
        if 'mentions' in post:
            for mention in post['mentions']:
                G.add_edge(post['author'], mention)
    nx.write_gexf(G, output_file)

if __name__ == "__main__":
    # Тестовые данные
    TEST_DATA = {
        "posts": [
            {
                "id": "1",
                "text": "Пример поста с #OSINT",
                "author": "@user1",
                "hashtags": ["OSINT"],
                "mentions": ["@user2"],
                "timestamp": "2023-01-01T12:00:00"
            },
            {
                "id": "2",
                "text": "Анализ данных #Python",
                "author": "@user2",
                "hashtags": ["Python"],
                "timestamp": "2023-01-01T12:05:00"
            }
        ]
    }

    with open('social_data.json', 'w', encoding='utf-8') as f:
        json.dump(TEST_DATA, f, indent=2)

    # Анализ
    posts = load_social_data('social_data.json')
    print("Топ хэштегов:", analyze_hashtags(posts).most_common(3))
    visualize_activity(posts)
    export_to_gexf(posts, 'social_graph.gexf')