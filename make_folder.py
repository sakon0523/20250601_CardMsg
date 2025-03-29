import os
import csv
import uuid

def create_folders_from_csv(csv_file):
    # スクリプトの実行ディレクトリを取得
    base_path = os.getcwd()

    # CSVファイルの絶対パスを取得
    csv_file_path = os.path.join(base_path, csv_file)

    if not os.path.exists(csv_file_path):
        print(f"CSVファイルが見つかりません: {csv_file_path}")
        return

    print(f"CSVファイルを読み込みます: {csv_file_path}")
    print(f"フォルダを作成するベースパス: {base_path}")

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 1:
                continue  # 空行をスキップ
            name = row[0].strip()  # 名前を取得
            folder_exists = False

            # ベースパス内の既存フォルダを確認
            for existing_folder in os.listdir(base_path):
                if existing_folder.startswith(name + "_"):
                    folder_exists = True
                    break

            if not folder_exists:
                # UUIDを生成してフォルダ名を作成
                new_uuid = str(uuid.uuid4())
                folder_name = f"{name}_{new_uuid}"
                folder_path = os.path.join(base_path, folder_name)

                # フォルダを作成
                os.makedirs(folder_path)
                print(f"フォルダを作成しました: {folder_path}")
            else:
                print(f"既存のフォルダが見つかりました: {name}_* のフォルダをスキップします")

if __name__ == "__main__":
    # CSVファイル名を指定（スクリプトと同じディレクトリに配置）
    csv_file_name = "input.csv"
    create_folders_from_csv(csv_file_name)