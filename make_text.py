from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError
import re
import pandas as pd
import xml.etree.ElementTree as ET
 
def create_query():
    """
    リクエストクエリの作成
    """
    # 国家基本政策委員会合同審査会（党首討論）1回分の発言を取得する
    params = {
        'nameOfMeeting': '国家基本政策委員会合同審査会',
        'maximumRecords': 1
        }
 
    return '&'.join(['{}={}'.format(key, value) for key, value in params.items()])
 
def parse_xml(res_xml):
    root = ET.fromstring(res_xml)
 
    try:
        # 取得したデータはPandasのデータフレームにする
        header = ['Date', 'Meeting', 'Speaker', 'Speech']
        df = pd.DataFrame(columns=header)
 
        for record in root.findall('./records/record/recordData/meetingRecord'):
            # 会議録情報の取得
            nameOfMeeting = record.find('nameOfMeeting').text
            issue = record.find('issue').text
            meeting = '{} {}'.format(nameOfMeeting, issue)
            date = record.find('date').text
            for speechRecord in record.findall('speechRecord'):
                # 発言者と発言の取得
                speaker = speechRecord.find('speaker').text
                speech = speechRecord.find('speech').text
                if speaker is not None:
                    # 先頭のspeechRecord（speechOrder=0）は出席者一覧などの会議録情報なのでスキップ
 
                    # 話者（speaker）を除去
                    # （拍手）など括弧でかこまれた箇所を除去
                    # 他人の発言中の発言〔～〕を除去
                    # 全角空白を除去（先頭に全角空白がある文がある）
                    speech = re.sub(r'\A○.*?君(）|)　|（.*?）|〔.*?〕|　', '', speech)
 
                    # データフレームに1行ずつ追加していく
                    row = [date, meeting, speaker, speech]
                    df.loc[len(df.index)] = row
 
        # 会議全体の発言をテキストファイルに保存
        # 鉢呂委員長は進行役なので除外
        with open('debate.txt', 'w') as f1:
            f1.write(''.join(df[df['Speaker'] != '鉢呂吉雄']['Speech'].tolist()))
 
        # 安倍首相の発言をテキストファイルに保存
        with open('abe.txt', 'w') as f2:
            f2.write(''.join(df[df['Speaker'] == '安倍晋三']['Speech'].tolist()))
    except ET.ParseError as e:
        print('ParseError: {}'.format(e.code))
 
def main():
    # クエリはパーセントエンコードしておく
    request_url = 'http://kokkai.ndl.go.jp/api/1.0/meeting?' + quote(create_query())
 
    req = Request(request_url)
 
    try:
        with urlopen(req) as res:
            res_xml = res.read().decode('utf8')
    except HTTPError as e:
        print('HTTPError: {}'.format(e.reason))
    except URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        parse_xml(res_xml)
 
if __name__ == '__main__':
    main()
