from PIL import Image, ImageDraw, ImageFont, ImageChops
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from io import BytesIO
import base64
import os


class Rollsign():

    def __init__(self, matrix):
        self.matrix = matrix
        self.images_dir = ""
        self.flist = []
        self.index = 0
    
    def __remove_background(self, image):
        r, g, b = image.split()
        src = (51, 51, 51)
        r = r.point(lambda p: 1 if p == src[0] else 0, mode="1")
        g = g.point(lambda p: 1 if p == src[1] else 0, mode="1")
        b = b.point(lambda p: 1 if p == src[2] else 0, mode="1")
        mask = ImageChops.logical_and(r, g)
        mask = ImageChops.logical_and(mask, b)
        image.paste(Image.new('RGB', (128, 32), (0, 0, 0)), mask=mask)
        return image
    
    def set_images_dir(self, images_dir):
        self.images_dir = images_dir
        # ディレクトリ内の画像を検索
        for file in os.listdir(self.images_dir):
            _, ext = os.path.splitext(file)
            if ext == '.png' or ext == '.bmp' or ext == '.jpg' or ext == '.gif':
                self.flist.append(file)
    
    def show(self, first = False):

        # 画像を表示
        if first == True:
            image_path = os.path.join(self.images_dir, self.flist[0])
        else:
            image_path = os.path.join(self.images_dir, self.flist[self.index])

        image = Image.open(image_path).convert('RGB')
        # 画像の縮小・背景除去
        image = image.resize((128, 32), Image.NONE)
        image = self.__remove_background(image)
        self.matrix.SetImage(image)

    def next_image(self):
        self.index += 1
        if self.index > len(self.flist) - 1:
            self.index = 0
        self.show()

    def prev_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.flist) - 1
        self.show()
    
    def get_base64_image(self):
        # エンコード用バッファ
        buffer = BytesIO()
        # 現在表示されている画像の表示
        image_path = os.path.join(self.images_dir, self.flist[self.index])
        image = Image.open(image_path)
        # 拡張子を抽出
        _, ext = os.path.splitext(image_path)  
        # base64エンコード
        image.save(buffer, format=ext.lstrip(".").upper())
        base64_image = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
        # Data URLを作成
        header = "data:image/{};base64,".format(ext.lstrip("."))
        return header + base64_image