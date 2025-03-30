import os
import qrcode
import re
from PIL import Image, ImageDraw, ImageFont

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
QR_SIZE = 300  # 各QRコードのサイズ
FONT_SIZE = 20  # フォントサイズ

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
                    box_size=10,
                    border=4,
                )
                qr.add_data(full_url)
                qr.make(fit=True)

                # QRコード画像を保存
                output_file = os.path.join(output_dir, f"{folder_name}.png")
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(output_file)
                print(f"QRコードを生成しました: {output_file}")

def create_a4_with_qr_codes(output_dir, output_file="qr_codes_a4.png"):
    # A4サイズの白いキャンバスを作成
    a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    draw = ImageDraw.Draw(a4_image)

    # QRコード画像を取得
    qr_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
    qr_files.sort()  # ファイル名でソート

    # QRコードを配置
    x, y = MARGIN, MARGIN
    for qr_file in qr_files:
        qr_path = os.path.join(output_dir, qr_file)
        qr_img = Image.open(qr_path).resize((QR_SIZE, QR_SIZE))  # QRコードをリサイズ
        a4_image.paste(qr_img, (x, y))  # QRコードを貼り付け

        # ファイル名（フォルダ名）を描画
        label = os.path.splitext(qr_file)[0]  # 拡張子を除いたファイル名
        text_bbox = draw.textbbox((0, 0), label, font=None)  # デフォルトフォントを使用
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x + (QR_SIZE - text_width) // 2
        text_y = y + QR_SIZE + 5  # QRコードの下に描画
        draw.text((text_x, text_y), label, fill="black")  # デフォルトフォントで描画

        # 次の位置を計算
        x += QR_SIZE + MARGIN
        if x + QR_SIZE + MARGIN > A4_WIDTH:  # 横幅を超えたら次の行へ
            x = MARGIN
            y += QR_SIZE + FONT_SIZE + MARGIN

        # 縦幅を超えた場合は警告
        if y + QR_SIZE + MARGIN > A4_HEIGHT:
            print("A4サイズに収まりきらないQRコードがあります。")
            break

    # A4画像を保存
    output_path = os.path.join(output_dir, output_file)
    a4_image.save(output_path)
    print(f"A4サイズのQRコード一覧を生成しました: {output_path}")

if __name__ == "__main__":
    # QRコードを生成
    generate_qr_codes(BASE_DIR, BASE_URL, OUTPUT_DIR)

    # A4サイズのQRコード一覧を生成
    create_a4_with_qr_codes(OUTPUT_DIR)