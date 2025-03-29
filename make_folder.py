import os
import csv
import uuid
import shutil

# CSVファイルのパス
csv_file_path = "input.csv"  # CSVファイル名を指定
base_path = os.getcwd()  # スクリプトの実行ディレクトリを基準にする
template_file_path = os.path.join(base_path, "_sample", "main.html")  # コピー元のテンプレートファイル

def create_folders_and_update_html(csv_file, base_path, template_file):
    if not os.path.exists(csv_file):
        print(f"CSVファイルが見つかりません: {csv_file}")
        return

    if not os.path.exists(template_file):
        print(f"テンプレートファイルが見つかりません: {template_file}")
        return

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 1:
                continue  # 空行をスキップ
            name = row[0].strip()  # 名前を取得
            folder_path = os.path.join(base_path, name)  # フォルダ名は名称のみ

            # フォルダが存在しない場合は作成
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"フォルダを作成しました: {folder_path}")
            else:
                print(f"フォルダが既に存在します: {folder_path}")

            # UUIDを生成してファイル名を作成
            new_uuid = str(uuid.uuid4())
            destination_file_path = os.path.join(folder_path, f"{new_uuid}.html")

            # main.html をコピーしてフォルダ内に保存
            shutil.copy(template_file, destination_file_path)

            # コピーしたファイル内のUUIDを置換
            with open(destination_file_path, mode="r", encoding="utf-8") as html_file:
                content = html_file.read()

            # UUIDを置換して保存
            content = content.replace("coro", new_uuid)  # 必要に応じて置換内容を調整
            with open(destination_file_path, mode="w", encoding="utf-8") as html_file:
                html_file.write(content)
            print(f"{new_uuid}.html をコピーして UUID を置換しました: {destination_file_path}")

if __name__ == "__main__":
    create_folders_and_update_html(csv_file_path, base_path, template_file_path)