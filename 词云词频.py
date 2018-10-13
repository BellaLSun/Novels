# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import jieba
import wordcloud
from scipy.misc import imread
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties



stop_list = pd.read_csv('./停用词.txt',engine='python',\
                        encoding='utf-8',names=['t'])['t'].tolist()
# 名字里有数字或字母就跟没看见一样。。。
f = open('./全职高手.txt',encoding='utf-8').read()
jieba.load_userdict('dict.txt')

def txt_cut(f):
    return [w for w in jieba.cut(f) if w not in stop_list and len(w)>1]

txtcut = txt_cut(f)

# 词频
word_count = pd.Series(txtcut).value_counts().sort_values(ascending=False)[0:20]

fig = plt.figure(figsize=(15,8))
x = word_count.index.tolist()
y = word_count.values.tolist()
sns.barplot(x, y, palette="BuPu_r")

font = FontProperties(fname='Songti.ttc')
bar_width = 0.5
plt.title('词频Top20')
plt.ylabel('count')
plt.xticks(rotation=50, fontproperties=font, fontsize=20)
plt.yticks(fontsize=20)
plt.title("words-frequency chart", fontproperties=font, fontsize=30)
sns.despine(bottom=True)
plt.savefig('./词频统计.png',dpi=400)
plt.show()


# 词云
fig = plt.figure(figsize=(15,5))
cloud = wordcloud.WordCloud(font_path='./FZSTK.TTF',
                            mask = imread('./background.jpeg'),
                            mode='RGBA',
                            background_color=None
                            ).generate(' '.join(txtcut))


img = imread('./color.png')
cloud_colors = wordcloud.ImageColorGenerator(np.array(img))
cloud.recolor(color_func=cloud_colors)


plt.imshow(cloud)
plt.axis('off')
plt.savefig('./wordcloud.png',dpi=1080)
plt.show()
