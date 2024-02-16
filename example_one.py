# coding : utf-8
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text_file = open("./speech.txt")
bindata = text_file.read()
txt = bindata

# text = WordCloud.__doc__
# wc = WordCloud(
#     background_color="white",
#     width=800,
#     height=600,
# )
# wc.generate(text)
# wc.to_file('wc1.png')

font_path = '/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
wordcloud = WordCloud(background_color="white",font_path = font_path ,width = 800,height = 600)
wordcloud.generate(txt)
wordcloud.to_file("./sample.png")

# plt.figure(figsize=(10,10))
# plt.imshow(wordcloud, interprolation="bilinear")
# plt.axis("off")
# plt.show()