import pandas as pd  # 数据处理包
import numpy as np  # 数据处理包
import json
from wordcloud import WordCloud  # 绘制词云
import jieba  # 中文分词包
import jieba.posseg as pseg
import re  # 正则表达式，可用于匹配中文文本
import collections  # 计算词频
import datetime
import time

numTops=10#出现次数前多少的词
def count_words(sentences):   #返回前三十出现最多次数的词
    filter_pattern = re.compile('[^\u4E00-\u9FD5]+')
    chinese_only = filter_pattern.sub('', sentences)
    words_list = pseg.cut(chinese_only)
    stopwords = [line.rstrip() for line in open('./stop-words.txt', 'r', encoding='utf-8')]
    meaninful_words = []
    for word, flag in words_list:
        if word not in stopwords:
            meaninful_words.append(word)
    word_counts = collections.Counter(meaninful_words)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(30)  # 获取前30最高频的词

    return word_counts_top

def write_injson(dates_proup,words):
    results=[]
    for j in range(0,len(dates_proup)):
        keys=['time']
        values=[]
        values.append(dates_proup[j])
        for val in words[j]:
            keys.append(val[0])
            values.append(val[1])
        temp_dic = dict(zip(keys, values))
        results.append(temp_dic)
    json_results=json.dumps(results,ensure_ascii=False,indent=4)
    with open("top-words.json", "w") as f:
        f.write(json_results)
    print("加载入文件完成...")

def screen(fathion_words):
    screen_fathion_words=[]
    for i in fathion_words:
        temp_f_w=[]
        for j in i:
            if len(j[0])>1:
                if(len(temp_f_w)<10):
                    temp_f_w.append(j)
        screen_fathion_words.append(temp_f_w)
    return screen_fathion_words
if __name__ == '__main__':
    comments = []
    with open('./LOLcomment.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    for dict1 in data:
        temp = []
        for value in dict1.values():
            temp.append(value)
        comments.append(temp)
    for i in range(0, len(comments)):
        timeStamp = comments[i][0]
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m", timeArray)
        comments[i][0]=otherStyleTime
    dates_proup=[]
    for i in comments:
        if i[0] not in dates_proup:
            dates_proup.append(i[0])
    fathion_words=[]
    for i in dates_proup:
        temp_words=""
        for j  in comments:
            if i== j[0]:
                temp_words+=j[1]
        fathion_words.append(count_words(temp_words))
    screen_fathion_words=screen(fathion_words)

    write_injson(dates_proup,screen_fathion_words)




