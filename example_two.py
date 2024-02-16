from wordcloud import WordCloud
import MeCab
 
# 取り込む品詞
cat1_list = ['名詞']
 
# 除外する品詞の詳細分類
cat2_list = ['代名詞', '非自立', '接尾']
 
m = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab')
m.parse('')
 
def word_wakati(text):
    """
    分かち書きテキストを返す
    """
    node = m.parseToNode(text)
    wd_list = []
    while node:
        cat1 = node.feature.split(',')[0]
        cat2 = node.feature.split(',')[1]
        if cat1 in cat1_list and cat2 not in cat2_list:
            wd_list.append(node.surface)
 
        node = node.next
 
    return ' '.join(wd_list)
 
def word_cloud_square(text_wakati):
    """
    ワードクラウドの作成
    """
    # font_pathに日本語フォントへのパスを指定する
    wc = WordCloud(background_color='white',
        font_path='/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf',
        width=500,height=500)
    wc.generate(text_wakati)
 
    wc.to_file("./make_image/wcloud_square.png")
 
def main():
    with open('debate.txt', 'r') as f1:
        debate = f1.read()
 
    debate_wakati = word_wakati(debate)
    word_cloud_square(debate_wakati)
 
if __name__ == '__main__':
    main()