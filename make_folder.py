import os
import csv
import uuid
import shutil
import re

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
        header = next(reader)
        for row in reader:
            if len(row) < 2:
                continue  # 空行をスキップ
            name = row[0].strip()  # 1列目: 名前
            link = row[1].strip()  # 2列目: リンク
            folder_path = os.path.join(base_path, name)  # フォルダ名は名称のみ

            # フォルダが存在しない場合は作成
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"フォルダを作成しました: {folder_path}")
            else:
                print(f"フォルダが既に存在します: {folder_path}")

            # link.html を確認してコピー
            link_file_path = os.path.join(folder_path, "link.html")
            if not os.path.exists(link_file_path):
                shutil.copy(os.path.join(base_path, "_sample", "link.html"), link_file_path)
                print(f"link.html をコピーしました: {link_file_path}")
            else:
                print(f"link.html は既に存在します: {link_file_path}")

            # link.html の中身を更新
            if os.path.exists(link_file_path):
                with open(link_file_path, mode="r", encoding="utf-8") as file:
                    content = file.read()
                # href="..." の部分を新しいリンクで置換
                content = re.sub(r'href=".*?"', f'href="{link}"', content)
                with open(link_file_path, mode="w", encoding="utf-8") as file:
                    file.write(content)
                print(f"link.html のリンクを更新しました: {link_file_path}")

            # message.html を確認してコピー
            message_file_path = os.path.join(folder_path, "message.html")
            if not os.path.exists(message_file_path):
                shutil.copy(os.path.join(base_path, "_sample", "message.html"), message_file_path)
                print(f"message.html をコピーしました: {message_file_path}")
            else:
                print(f"message.html は既に存在します: {message_file_path}")

            # UUID.html ファイルを探して中身を更新
            existing_html_file = None
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".html") and file_name not in ["link.html", "message.html"]:
                    existing_html_file = os.path.join(folder_path, file_name)
                    break

            if existing_html_file:
                # 既存のUUID.htmlファイルがある場合、中身を更新
                print(f"既存のUUID HTMLファイルを更新します: {existing_html_file}")
                with open(template_file, mode="r", encoding="utf-8") as template:
                    content = template.read()
                # UUIDを置換して保存
                uuid_value = os.path.splitext(os.path.basename(existing_html_file))[0]
                content = content.replace("coro", uuid_value)
                with open(existing_html_file, mode="w", encoding="utf-8") as html_file:
                    html_file.write(content)
            else:
                # 新しいUUIDを生成してファイルを作成
                new_uuid = str(uuid.uuid4())
                destination_file_path = os.path.join(folder_path, f"{new_uuid}.html")
                shutil.copy(template_file, destination_file_path)
                print(f"新しいUUID HTMLファイルを作成しました: {destination_file_path}")

                # コピーしたファイル内のUUIDを置換
                with open(destination_file_path, mode="r", encoding="utf-8") as html_file:
                    content = html_file.read()
                content = content.replace("coro", new_uuid)
                with open(destination_file_path, mode="w", encoding="utf-8") as html_file:
                    html_file.write(content)

if __name__ == "__main__":
    create_folders_and_update_html(csv_file_path, base_path, template_file_path)