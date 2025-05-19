import csv
import json
from collections import defaultdict

# 入力CSVと出力JSONのファイル名
csv_file = 'guests.csv'
json_file = 'guests.json'

# デフォルト辞書でテーブル番号ごとにリストを作成
guest_data = defaultdict(list)

# CSV読み込み
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 3:
            continue  # 不完全な行はスキップ
        name, role, table = row[0].strip(), row[1].strip(), row[2].strip()
        guest_data[table].append({
            'role': role,
            'name': name
        })

# JSON出力
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(guest_data, f, ensure_ascii=False, indent=2)

print(f'変換完了: {json_file}')