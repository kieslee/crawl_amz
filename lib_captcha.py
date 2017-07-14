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
    return img
    img = img.convert('RGBA')
    img = binarize_image(img)
    img = img.convert('L')
    return img

def binarize_image(img):
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 100 or pixdata[x,y][1] < 100 or pixdata[x,y][2] < 100:
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                pixdata[x, y] = (255,255,255,255)
    return img

def image_to_text(img):
    return tesseract(img)

def tesseract(img):
    text = pytesseract.image_to_string(img)
    text = re.sub('[\W]', '', text)
    return text

def parse_captcha(url):
    data = url_to_image_data(url)
    img_file = open('/tmp/captcha.jpg', 'w')
    img_file.write(data)
    img_file.close()
    img = image_data_to_tiff(data)
    text = image_to_text(img)
    return text
