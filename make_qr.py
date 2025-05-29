import os
import qrcode
import re
from PIL import Image, ImageDraw, ImageFont
import csv

# CSVファイルのパス
CSV_FILE = os.path.join("input.csv")

# ベースURL
BASE_URL = "https://my0601.com/"

# 検索するディレクトリ
BASE_DIR = os.getcwd()  # 現在の作業ディレクトリを基準にする

# QRコードを保存するディレクトリ
OUTPUT_DIR = os.path.join(BASE_DIR, "qr_codes")
os.makedirs(OUTPUT_DIR, exist_ok=True)  # 保存先ディレクトリを作成

# A4サイズのピクセル数 (300 DPI)
A4_WIDTH = 2480  # 横幅 (8.27インチ × 300 DPI)
A4_HEIGHT = 3508  # 縦幅 (11.69インチ × 300 DPI)
MARGIN = 50  # 余白
START_MARGIN = 80  # 余白
QR_SIZE = 400  # 各QRコードのサイズ
FONT_SIZE = 20  # フォントサイズ
TATESEN = 1000  # 余白

# フォントサイズを変更
FONT_SIZE = 40  # フォントサイズを大きくする
FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"  # 日本語対応フォントのパス

def generate_qr_codes(base_dir, base_url, output_dir):
    for root, dirs, files in os.walk(base_dir):
        for folder_name in dirs:
            # フォルダ名を取得
            folder_path = os.path.join(root, folder_name)
            
            # 対象のUUID形式のHTMLファイルを検索
            html_files = [
                f for f in os.listdir(folder_path)
                if f.endswith(".html") and f not in ["link.html", "message.html"]
            ]
            for html_file in html_files:
                # リンクを生成
                relative_path = os.path.join(folder_name, html_file)
                full_url = os.path.join(base_url, relative_path)

                # QRコードを生成
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=8,
                    border=4,
                )
                qr.add_data(full_url)
                qr.make(fit=True)

                # QRコード画像を保存
                output_file = os.path.join(output_dir, f"{folder_name}.png")
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(output_file)
                print(f"QRコードを生成しました: {output_file}")

def load_team_data(csv_file):
    """CSVファイルからフォルダ名とチーム名、日本語名の対応を読み込む"""
    team_data = {}
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 'name'列をキーにして、'team'列と'name_jp'列を値として格納
            team_data[row["name"]] = {
                "team": row["team"],
                "name_jp": row["name_jp"]
            }
    return team_data

def create_a4_with_qr_codes(output_dir, output_file_prefix="qr_codes_page"):
    # チームデータを読み込む
    team_data = load_team_data(CSV_FILE)
    print("チームデータ:", team_data)

    # QRコード画像を取得
    qr_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
    qr_files.sort()  # ファイル名でソート

    page_number = 1
    x, y = START_MARGIN, START_MARGIN
    a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    draw = ImageDraw.Draw(a4_image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)  # 日本語対応フォントを指定

    is_new_page = True
    is_second_iine = False
    add_x = 0

    for qr_file in qr_files:
        if is_new_page:
            for x_pos in range(MARGIN, A4_WIDTH - MARGIN, 10):  # 点線を10px間隔で描画
                draw.line((x_pos, START_MARGIN, x_pos + 5, START_MARGIN), fill="black", width=1)
            # 現在のページのx座標=900に縦の点線を描画
            for y_pos in range(MARGIN, A4_HEIGHT - MARGIN, 10):
                draw.line((TATESEN, y_pos, TATESEN, y_pos + 5), fill="black", width=1)
            is_new_page = False

        if is_second_iine:
            for y_pos in range(MARGIN, A4_HEIGHT - MARGIN, 10):
                draw.line((TATESEN*2, y_pos, TATESEN*2, y_pos + 5), fill="black", width=1)
            add_x = TATESEN

        qr_path = os.path.join(output_dir, qr_file)
        qr_img = Image.open(qr_path).resize((QR_SIZE, QR_SIZE))  # QRコードをリサイズ
        qr_img_pos_x = x + add_x
        qr_img_pos_y = y + MARGIN - 30
        a4_image.paste(qr_img, (qr_img_pos_x, qr_img_pos_y))  # QRコードを貼り付け

        # ファイル名（フォルダ名）を描画
        label = os.path.splitext(qr_file)[0]  # 拡張子を除いたファイル名
        team_info = team_data.get(label, {"team": "Unknown", "name_jp": ""})
        team_name = team_info["team"]
        name_jp = team_info["name_jp"] + ' 様'
        text_bbox = draw.textbbox((0, 0), name_jp, font=font)  # 日本語対応フォントを使用
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (QR_SIZE - text_width) // 2 + add_x
        text_y = y + QR_SIZE + 10  # QRコードの下に描画
        draw.text((text_x, text_y), name_jp, fill="black", font=font)

        # チーム名を描画（QRコードの右側）
        hashtags_list = [f"#{tag}" for tag in team_name.split("/")]  # ハッシュタグ形式に変換
        hashtags = "\n".join([" ".join(hashtags_list[i:i+1]) for i in range(0, len(hashtags_list), 1)])  # 2個ずつ改行
        team_text_x = x + QR_SIZE + add_x  # QRコードの右側に配置
        team_text_y = qr_img_pos_y + 50  # QRコードの上部に揃える
        draw.text((team_text_x, team_text_y), hashtags, fill="black", font=font)

        # passを記載
        pass_text = "pass: my0601"
        draw.text((team_text_x, team_text_y+250), pass_text, fill="black", font=font)

        # 点線を描画（フォルダ名の下）
        dotted_line_y = y + QR_SIZE + 100  # フォルダ名の下に点線を描画
        for x_pos in range(MARGIN, A4_WIDTH - MARGIN, 10):  # 点線を10px間隔で描画
            draw.line((x_pos, dotted_line_y, x_pos + 5, dotted_line_y), fill="black", width=1)

        # 次の位置を計算（縦方向に移動）
        y = dotted_line_y

        # 縦幅を超えた場合は次のページを作成
        if y + QR_SIZE + MARGIN + 100 > A4_HEIGHT:
            if is_second_iine:
                is_second_iine = False
                add_x = 0
                # 現在のページを保存
                output_path = os.path.join(output_dir, f"{output_file_prefix}_{page_number}.png")
                a4_image.save(output_path)

                # 次のページを作成
                page_number += 1
                y = START_MARGIN  # 上余白にリセット
                a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
                draw = ImageDraw.Draw(a4_image)
                is_new_page = True
            else:
                is_second_iine = True
                y = START_MARGIN  # 上余白にリセット

    # 最後のページを保存
    if y > START_MARGIN:  # 最後のページに内容がある場合のみ保存
        output_path = os.path.join(output_dir, f"{output_file_prefix}_{page_number}.png")
        a4_image.save(output_path)
        print(f"A4サイズのQRコード一覧を生成しました: {output_path}")

def save_as_pdf(output_dir, pdf_file="qr_codes.pdf"):
    # A4ページ画像を取得（qr_codes_page_*.png のみ）
    qr_pages = [f for f in os.listdir(output_dir) if f.startswith("qr_codes_page_") and f.endswith(".png")]
    qr_pages.sort()  # ファイル名でソート

    # 画像をPDFに変換
    images = []
    for qr_page in qr_pages:
        qr_path = os.path.join(output_dir, qr_page)
        img = Image.open(qr_path).convert("RGB")  # RGBモードに変換
        images.append(img)

    # PDFとして保存
    if images:
        pdf_path = os.path.join(output_dir, pdf_file)
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"PDFを生成しました: {pdf_path}")
    else:
        print("QRコードページ画像が見つかりませんでした。")

if __name__ == "__main__":
    # QRコードを生成
    generate_qr_codes(BASE_DIR, BASE_URL, OUTPUT_DIR)

    # A4サイズのQRコード一覧を生成
    create_a4_with_qr_codes(OUTPUT_DIR)
    
    # QRコード一覧をPDFに変換
    save_as_pdf(OUTPUT_DIR)