from lib_captcha import parse_captcha
import sys

text = parse_captcha(sys.argv[1])
print text