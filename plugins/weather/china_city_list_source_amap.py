from os import path

with open(path.join(path.dirname(__file__), 'china_city_list_source_amap.txt'), 'r', encoding='utf-8') as f:
    CHINESE_CITIES = { line.strip('\n') for line in f }
