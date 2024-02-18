# coding : utf-8
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text_file = open("./speech.txt")
bindata = text_file.read()
txt = bindata


font_path = '/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
wordcloud = WordCloud(background_color="white",font_path = font_path ,width = 800,height = 600)
wordcloud.generate(txt)
wordcloud.to_file("./sample.png")
