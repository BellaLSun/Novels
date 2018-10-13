# -*- coding: utf-8 -*-

import jieba,codecs
import jieba.posseg as pseg
import pandas as pd

'''
遍历文本每一行，再提取每一行中出现的人物，
如果两个人物同时出现在同一行，那么他们之间人物关系密切度+1，
最后，密切度最高的为最佳CP。
'''
names = {} #提取的人名，和出现的频数。
relationships = {} #提取的人物关系。
lineNames = []#每一行提取的人名，做缓存处理。

'''
一份小说特殊词库
搜狗细胞词库可以下载小说对应的词库
网址：https://pinyin.sogou.com/dict/
'''
jieba.load_userdict('dict.txt')


'''
codecs库：用来读取文本时，防止文本编码不统一，造成错误；
jieba.posseg：分词后显示词性。
'''
# 添加名字
with codecs.open('全职高手.txt','r','utf8') as f:
    n = 0
    for line in f.readlines(): 
        n+=1
        print('正在读取第{}行'.format(n))
        poss = pseg.cut(line)
        # 每一行中出现的人名后边 +[]
        lineNames.append([])
        for w in poss:
            if w.flag != 'nr' or len(w.word) < 2 or len(w.word) > 3:
                #排除词性不为nr(人名)，长度大于3小于2的所有词汇
                continue
            # gets the last element
            lineNames[-1].append(w.word)#以行为组，保存每行所提取的人名
            # 如果这一行没有名字，则set to 0；
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {} #把所涉及的人名作为键添加入关系字典
            # 如果这一行没有名字，则频数+1
            names[w.word] += 1

# 添加关系
for line in lineNames:
    for name1 in line:
        for name2 in line:
            if name1 == name2:#名称相同，排除
                continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2]= 1#对于新的人物关系，生成新的键值对。
            else:
                relationships[name1][name2] = relationships[name1][name2]+ 1
                #对于已有的人物关系，密切度+1
                
                
node = pd.DataFrame(columns=['Id','Label','Weight'])
edge = pd.DataFrame(columns=['Source','Target','Weight'])

# The method items() returns a list of dict's (key, value) tuple pairs
for name,times in names.items():
        node.loc[len(node)] = [name,name,times]

for name,edges in relationships.items():
        for v, w in edges.items():
            # 两人关系被提到3词以上
            if w > 3:
                edge.loc[len(edge)] = [name,v,w]
                
edge.to_csv('./edge(原).csv',index=0)
node.to_csv('./node(原).csv',index=0)

#And then, 把数据csv导入Gephi
