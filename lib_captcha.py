# -*- coding:utf-8 -*-

from cStringIO import StringIO
import urllib
import re
from PIL import Image
import pytesseract


def url_to_image_data(url):
    data = None
    try:
        stream = urllib.urlopen(url)
        data = stream.read()
    finally:
        stream.close()

    return data


def image_data_to_tiff(data):
    img = Image.open(StringIO(data))

    # img = img.convert('RGBA')
    img = img.convert('L')
    img = binarize_image(img)
    return img


def binarize_image(img):
    return img.point(initTable(), '1')


def initTable(threshold=140):           # 二值化函数
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


def image_to_text(img):
    return tesseract(img)


def tesseract(img):
    text = pytesseract.image_to_string(img)
    #text = re.sub('[\W]', '', text)
    return text


def parse_captcha(url):
    data = url_to_image_data(url)
    # img_file = open('/tmp/captcha.jpg', 'w')
    # img_file.write(data)
    # img_file.close()
    img = image_data_to_tiff(data)
    text = image_to_text(img)
    return text
