from PIL import Image, ImageDraw, ImageFont, ImageChops
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import os
import ipget
import subprocess
import time

#画像を128 * 32に正規化
def shape_image(img):
    img = img.resize((128, 32), Image.NONE)
    r, g, b = img.split()
    src = (51,51,51)
    r = r.point(lambda p: 1 if p == src[0] else 0, mode="1")
    g = g.point(lambda p: 1 if p == src[1] else 0, mode="1")
    b = b.point(lambda p: 1 if p == src[2] else 0, mode="1")
    mask = ImageChops.logical_and(r,g)
    mask = ImageChops.logical_and(mask, b)
    img.paste(Image.new('RGB', (128,32), (0,0,0)), mask = mask)
    return img

#文字画像を生成
def make_string_image(text, color):
    imgOut = Image.new('RGB', (128,16), (0, 0, 0))
    imgStr = Image.new('1', (128, 16), 0)
    font = ImageFont.truetype("fonts/JF-Dot-Izumi16B.ttf",16)
    draw = ImageDraw.Draw(imgStr)
    draw.text((0,0), text = text, fill = 1, font = font)
    imgOut.paste(Image.new('RGB',(128, 16), color), mask = imgStr)
    return imgOut

if __name__ == "__main__":

    #マトリクスの初期化
    options = RGBMatrixOptions()
    options.hardware_mapping = 'adafruit-hat'
    options.rows=32
    options.cols=128
    options.brightness = 50
    options.gpio_slowdown=4
    options.pwm_lsb_nanoseconds = 100
    matrix = RGBMatrix(options = options)

    #管理ページのアドレスを表示
    ip = ipget.ipget()
    plt = Image.new('RGB', (128,32), (0,0,0))
    plt.paste(make_string_image("管理ページ:", (255,160,0)), (20,0))
    plt.paste(make_string_image(ip.ipaddr('wlan0').split('/')[0], (181, 255, 0)), (16,16))
    matrix.SetImage(plt)
    wait = input()

    flist = list()
    for file in os.listdir('/media/usb0'):
        name, ext = os.path.splitext(file)
        if ext == '.png' or ext == '.bmp' or ext == '.jpg' or ext == '.gif':
            flist.append(file)
    while True:
        for file in flist:
            img = Image.open("/media/usb0/" + file).convert('RGB')
            img = shape_image(img)
            matrix.SetImage(img)
            skip = input()
    
