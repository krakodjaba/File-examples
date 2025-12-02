"""
geo_examples.py

Примеры работы с геоданными в OSINT:
- Чтение GPX, создание KML.
- Извлечение точек, анализ высот.
- Конвертация в CSV.
"""

import gpxpy
import simplekml
import pandas as pd

# Тестовые данные (упрощённый GPX)
TEST_GPX_DATA = """<?xml version="1.0"?>
<gpx><trk><trkseg>
<trkpt lat="45.0" lon="-122.0"><ele>100</ele></trkpt>
<trkpt lat="46.0" lon="-123.0"><ele>200</ele></trkpt>
</trkseg></trk></gpx>
"""

def read_gpx(filepath):
    """Чтение GPX-файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return gpxpy.parse(f)

def gpx_to_csv(gpx_filepath, csv_filepath):
    """Экспорт GPX в CSV."""
    gpx = read_gpx(gpx_filepath)
    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append({"lat": point.latitude, "lon": point.longitude, "ele": point.elevation})
    pd.DataFrame(data).to_csv(csv_filepath, index=False)

if __name__ == "__main__":
    # Примеры использования
    with open("test_data.gpx", 'w', encoding='utf-8') as f:
        f.write(TEST_GPX_DATA)
    gpx_to_csv("test_data.gpx", "test_data.csv")