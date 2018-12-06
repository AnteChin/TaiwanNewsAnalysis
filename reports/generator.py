import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import special_dict
from collections import Counter
from chinesetrans.langconv import *
from PIL import Image
import re
import matplotlib

FILE_PATH = '自由时报正文分詞.xlsx'
TYPE_NAME = 'context'  # context or title


def getFrequence(frame, sheetname, index_name, word_cloud=False, word_cloud_name='test.png', frequence=True):
    '''
    得到报道中关键词的出现次数和词频
    :param frame: pandas中的 Dataframe 数据类型
    :param sheetname: 输出表单名
    :param index_name: dataframe中的索引名
    :param word_cloud: 是否需要生成词云
    :param frequence: 是否获取词频
    :return: NULL
    '''
    raw_title = ''
    for i in range(0, frame.index.size):
        raw_title += frame[index_name][i] + ' '
    #  繁體轉簡體，因為fenci包不兼容繁體
    st_word = Traditional2Simplified(raw_title)
    cut_title = jieba.cut(st_word, cut_all=False)
    output_titles = []
    for i in cut_title:
        if not isinstance(i, str):
            i = str(i)
        #  簡體轉繁體
        i = Simplified2Traditional(i)
        if i in special_dict.replace_list:
            i = special_dict.replace_list[i]
        if i not in special_dict.banlist:
            output_titles.append(i)
    if word_cloud is True:
        generateWordCloud(' '.join(output_titles), word_cloud_name)
    top_title = Counter(output_titles).most_common(300)  # 找出出现频率最高的词
    cipin = pd.DataFrame(top_title, columns=['关键词', '出现次数'])
    if frequence is True:
        total_reports = frame.index.size
        cipin['词频'] = cipin['出现次数'] / total_reports
    cipin.to_excel(writer, sheet_name=sheetname, index=False)


def generateWordCloud(string, filename):
    stopwords = set(STOPWORDS)
    stopwords.add(" ")
    coloring = np.array(Image.open("../resource/taiwan.jpg"))
    # create coloring from image
    image_colors = ImageColorGenerator(coloring)
    font = r'C:\Windows\Fonts\msyh.ttc'
    wc = WordCloud(background_color="white", max_words=100, mask=coloring, width=800, height=600,
                   max_font_size=70, random_state=32, font_path=font, scale=32)
    wc.generate(string)
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.figure(figsize=(60, 75))  # 清晰度
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()
    wc.to_file(filename)


def changeDateFormat(frame):
    #  将 xxxx年xx月xx日变为  xxxx-xx-xx
    for i in range(0, frame.index.size):
        t = re.findall(r"\d+\.?\d*", frame['date'][i])
        frame['date'][i] = np.datetime64(t[0]+'-'+t[1]+'-'+t[2])


frame = pd.read_excel('ltn.xlsx', columns=['title', 'date', 'context'],
                      dtype={'title': np.str, 'date': np.str, 'context': np.str})
changeDateFormat(frame)
frame[['date']] = frame[['date']].astype(np.datetime64)
frame['date'] = frame['date'].dt.date
writer = pd.ExcelWriter(FILE_PATH)
getFrequence(frame=frame, sheetname="All", index_name=TYPE_NAME, word_cloud=False, frequence=False)
# 將新聞按日期分，每個日期設為一個dataframe
group_by_date = frame.groupby('date')
info = group_by_date.size()
info.to_excel(writer, sheet_name='報道數量', index=True)
dates = list(group_by_date.groups.keys())
for date in dates:
    df = group_by_date.get_group(str(date))
    df = df.reset_index(drop=True)
    getFrequence(df, sheetname=str(date), index_name=TYPE_NAME, word_cloud=False, frequence=False)
writer.save()

