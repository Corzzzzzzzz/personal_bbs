from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, string
import os

class Captcha():
    # 四位验证码
    num = 4
    # 图片验证码宽高
    size = (100, 30)
    # 字体大小
    fontsize = 25
    # 干扰线数量
    line_number = 2

    #构造验证码源文本
    source = list(string.ascii_letters)
    source.extend([str(i) for i in range(10)])

    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        """set a random color"""
        random.seed()
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Courgette-Regular.ttf',
            'LHANDW.TTF',
            'Lobster-Regular.ttf',
            'verdana.ttf'
        ]
        font = random.choice(fonts)
        return 'utils/captcha'+font

    @classmethod
    def gene_text(cls, number):
        return ''.join(random.sample(cls.source, number))

    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())



    @classmethod
    def gene_graph_captcha(cls):
        """生成验证码的类方法"""
        #set the width and height of captcha
        width, height = cls.size
        #create an image
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        #choose a font type and font size
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        #create draw and involve to the image
        draw = ImageDraw.Draw(image)
        #create random captcha text
        text = cls.gene_text(cls.num)
        #get font size
        font_width, font_height = font.getsize(text)
        #draw captcha text in image
        draw.text(((width - font_width)/2, (height - font_height)/2), text=text, font=font, fill=cls.__gene_random_color(150, 255))
        #draw disturb line
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        #draw disturb points
        cls.__gene_points(draw, 10, width, height)

        return text, image






