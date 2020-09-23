from PIL import Image, ImageDraw, ImageFont, ImageChops
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from io import BytesIO
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import base64
import os

images_dir = "images"
index = 0


def remove_background(image):
    r, g, b = image.split()
    src = (51, 51, 51)
    r = r.point(lambda p: 1 if p == src[0] else 0, mode="1")
    g = g.point(lambda p: 1 if p == src[1] else 0, mode="1")
    b = b.point(lambda p: 1 if p == src[2] else 0, mode="1")
    mask = ImageChops.logical_and(r, g)
    mask = ImageChops.logical_and(mask, b)
    image.paste(Image.new('RGB', (128, 32), (0, 0, 0)), mask=mask)
    return image


def make_string_image(text, color):
    imageOut = Image.new('RGB', (128, 16), (0, 0, 0))
    imageStr = Image.new('1', (128, 16), 0)
    font = ImageFont.truetype("static/fonts/JF-Dot-Izumi16B.ttf", 16)
    draw = ImageDraw.Draw(imageStr)
    draw.text((0, 0), text=text, fill=1, font=font)
    imageOut.paste(Image.new('RGB', (128, 16), color), mask=imageStr)
    return imageOut


def image2base64(image):
    buffer = BytesIO()
    _, ext = os.path.splitext(image_path)  # 拡張子を抽出
    image.save(buffer, format=ext.lstrip(".").upper())
    base64_image = base64.b64encode(
        buffer.getvalue()).decode().replace("'", "")
    header = "data:image/{};base64,".format(ext.lstrip("."))
    return header + base64_image


def auto_switch():
    global index
    index += 1
    if index > len(flist) - 1:
        index = 0
    image_path = os.path.join(images_dir, flist[index])
    image = Image.open(image_path).convert('RGB').resize((128, 32), Image.NONE)
    matrix.SetImage(remove_background(image))


if __name__ == "__main__":

    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_switch, "interval", seconds=30, id="auto_switch")
    scheduler.start(paused=True)

    # マトリクスの初期化
    options = RGBMatrixOptions()
    options.hardware_mapping = 'adafruit-hat'
    options.rows = 32
    options.cols = 128
    options.brightness = 50
    options.gpio_slowdown = 4
    options.pwm_lsb_nanoseconds = 100
    matrix = RGBMatrix(options=options)

    # ディレクトリ内の画像を検索
    flist = []
    for file in os.listdir(images_dir):
        name, ext = os.path.splitext(file)
        if ext == '.png' or ext == '.bmp' or ext == '.jpg' or ext == '.gif':
            flist.append(file)

    # 最初の画像を表示
        image_path = os.path.join(images_dir, flist[index])
        image = Image.open(image_path).convert('RGB')
        # 画像の縮小・背景除去
        image = image.resize((128, 32), Image.NONE)
        image = remove_background(image)
        matrix.SetImage(image)

    while True:

        cmd = input()  # Flask(app.py)から標準入力で受ける

        #次の画像, 前の画像
        if cmd == "next" or cmd == "prev":
            if cmd == "next":
                index += 1
                if index > len(flist) - 1:
                    index = 0
            elif cmd == "prev":
                index -= 1
                if index < 0:
                    index = len(flist) - 1

            # 画像の読み込み
            image_path = os.path.join(images_dir, flist[index])
            image = Image.open(image_path).convert('RGB')
            # 画像をbase64エンコードしてFlaskへ
            print(image2base64(image))
            # 画像の縮小・背景除去
            image = image.resize((128, 32), Image.NONE)
            image = remove_background(image)
            matrix.SetImage(image)

        # 自動切り替えの有無
        elif cmd.split(',')[0] == "auto_switch" or cmd == "manual":

            if cmd.split(',')[0] == "auto_switch":
                interval = cmd.split(',')[1]
                scheduler.reschedule_job(
                    "auto_switch", trigger="interval", seconds=int(interval))
                scheduler.resume()

            elif cmd == "manual":
                scheduler.pause()

        elif cmd == "image":
            # 画像の読み込み
            image_path = os.path.join(images_dir, flist[index])
            image = Image.open(image_path).convert('RGB')
            # 画像をbase64エンコードしてFlaskへ
            print(image2base64(image))
