from wordcloud import WordCloud
 
FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
TXT_NAME = "debate"
 
 
def get_word_str(text):
    import MeCab
    import re
 
    mecab = MeCab.Tagger()
    parsed = mecab.parse(text)
    lines = parsed.split('\n')
    lines = lines[0:-2]
    word_list = []
 
    for line in lines:
        tmp = re.split('\t|,', line)
 
        # 名詞のみ対象
        if tmp[1] in ["名詞"]:
            # さらに絞り込み
            if tmp[2] in ["一般", "固有名詞"]:
                word_list.append(tmp[0])
 
    return " " . join(word_list)
 
 
# テキストファイル読み込み
read_text = open(TXT_NAME + ".txt", encoding="utf8").read()
 
# 文字列取得
word_str = get_word_str(read_text)
 
# 画像作成
wc = WordCloud(font_path=FONT_PATH, 
               width=600,  # 幅
               height=400,  # 高さ
               prefer_horizontal=1,  # 横書きで配置することを試す確率 (デフォルト0.9)
               background_color='black',  # 背景色
               include_numbers=True,  # 数値だけの単語も含む
               colormap='tab20',  # 文字色のカラーマップ指定
               regexp=r"[\w']+",  # 一文字の単語も含む
            ).generate(word_str)
 
# 画像保存（テキストファイル名で）
wc.to_file(TXT_NAME + ".png")