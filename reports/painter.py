import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


frame = pd.read_excel('自由时报标题分詞.xlsx', sheet_name='報道數量')
frame['date'] = frame['date'].dt.date
frame.columns = ['date', 'counts']
dates = []
for i in range(0, frame.index.size):
    if frame.iloc[i]['counts'] >= 30.0:
        dates.append(frame.iloc[i]['date'])
gaoxiong = {'日期': [], '韓國瑜': [], '陳其邁': []}
taipei = {'日期': [], '丁守中': [], '柯文哲': [], '姚文智': []}
for date in dates:
    df = pd.read_excel('自由时报标题分詞.xlsx', sheet_name=str(date))
    df.columns = ['keywords', 'counts', 'frequency']
    df = df.set_index('keywords', drop=True)
    gaoxiong['日期'].append(date)
    taipei['日期'].append(date)
    if '韓國瑜' not in df.index:
        gaoxiong['韓國瑜'].append(0.0)
    else:
        gaoxiong['韓國瑜'].append(df.loc['韓國瑜'].frequency)
    if '陳其邁' not in df.index:
        gaoxiong['陳其邁'].append(0.0)
    else:
        gaoxiong['陳其邁'].append(df.loc['陳其邁'].frequency)
    if '丁守中' not in df.index:
        taipei['丁守中'].append(0.0)
    else:
        taipei['丁守中'].append(df.loc['丁守中'].frequency)
    if '柯文哲' not in df.index:
        taipei['柯文哲'].append(0.0)
    else:
        taipei['柯文哲'].append(df.loc['柯文哲'].frequency)
    if '姚文智' not in df.index:
        taipei['姚文智'].append(0.0)
    else:
        taipei['姚文智'].append(df.loc['姚文智'].frequency)

df_gaoxiong = pd.DataFrame(gaoxiong)
df_gaoxiong = df_gaoxiong.set_index('日期', drop=True)

df_taipei = pd.DataFrame(taipei)
df_taipei = df_taipei.set_index('日期', drop=True)

plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
df_gaoxiong.plot(kind='bar', figsize=(9, 9), grid=True, title='自由時報高雄市候選人詞頻對比圖', fontsize=12, colormap='brg')
plt.savefig("自由時報-高雄.jpg")
df_taipei.plot(kind='bar', figsize=(12, 12), grid=True, title='自由時報台北市候選人詞頻對比圖', fontsize=12, colormap='brg')
plt.savefig("自由時報-台北.jpg")
