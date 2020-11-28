# c处理lol
import pandas as pd  # 数据处理包
import numpy as np  # 数据处理包
import json
from wordcloud import WordCloud  # 绘制词云,无用
import jieba  # 中文分词包
import jieba.posseg as pseg
import re  # 正则表达式，可用于匹配中文文本
import collections  # 计算词频
import datetime
import time
import csv

numTops = 10  # 出现次数前多少的词，可认人为设置
source_data_path = './LOLcomment-SuNing.json'
output_path = "top-words-sn.json"
csv_out_path = 'top-words-sn.csv'


def count_words(sentences):  # 返回前100出现最多次数的词
    filter_pattern = re.compile('[^\u4E00-\u9FD5]+')  # 使用中文正则表达式
    chinese_only = filter_pattern.sub('', sentences)
    words_list = pseg.cut(chinese_only)  # 分词
    stopwords = [line.rstrip() for line in open('./stop-words.txt', 'r', encoding='utf-8')]  # 读取停用词：无用的词
    meaninful_words = []  # 存放经过筛选除去停用词的词
    for word, flag in words_list:
        if word not in stopwords:
            meaninful_words.append(word)
    word_counts = collections.Counter(meaninful_words)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(100)  # 获取前100最高频的词,再从里面筛选挑选符合添加的前numTOP个

    return word_counts_top  # 返回前100的词


def write_injson(dates, words):  # 把结果写进json
    results = []
    for m in range(0, len(dates)):
        keys = ['time']
        values = [dates[m]]
        for val in words[m]:
            keys.append(val[0])
            values.append(val[1])
        temp_dic = dict(zip(keys, values))  # 把两个数组合成一个
        results.append(temp_dic)
    json_results = json.dumps(results, ensure_ascii=False, indent=4)  # 转变为json
    with open(output_path, "w") as f:  # 写json文件
        f.write(json_results)
    print("写进json完成")


def screen(words):  # 筛选部分热词，现在只是对长度为1的进行了清洗，如有需要可以再加
    screen_Fathion_Words = []
    for m in words:
        temp_f_w = []
        for n in m:
            if len(n[0]) > 1:
                if len(temp_f_w) < numTops:  # 把长度为1词的剔除
                    temp_f_w.append(n)
        screen_Fathion_Words.append(temp_f_w)
    return screen_Fathion_Words


def write_incsv(dates, words):
    firstline = ["词", "时间", "频数"]
    contents = [firstline]
    for m in range(0, len(words)):
        for n in words[m]:
            temp_line = [n[0], dates[m], n[1]]
            contents.append(temp_line)
    csvFile = open(csv_out_path, "w")  # 创建csv文件
    writer = csv.writer(csvFile)  # 创建写的对象
    # 写入多行用writerows                                #写入多行
    writer.writerows(contents)
    csvFile.close()
    print("写进csv完成")


def read_json1(path):  # 读取json文件
    comment = []
    with open(path, 'r', encoding='UTF-8') as f:  # 读取数据源
        data = json.load(f)
    # 读进一个二维数组里
    for dict1 in data:
        temp = []
        for value in dict1.values():
            temp.append(value)
        comment.append(temp)
    # 对时间戳进行转换为标准时间
    for m in range(0, len(comment)):
        timeStamp = comment[m][0]
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        # 对日期进行周处理，一个月分4周，前三周7天，第四周多2-3天
        timeByWeek = otherStyleTime[0:-2]
        which_week = (int(otherStyleTime[-2]) * 10 + int(otherStyleTime[-1])) // 7 + 1
        if which_week > 4:
            which_week = 4
        timeByWeek += str(0)
        timeByWeek += str(which_week)
        comment[m][0] = timeByWeek
    return comment


if __name__ == '__main__':
    comments = read_json1(source_data_path)
    # 对时间进行去重分组
    dates_group = []
    for i in comments:
        if i[0] not in dates_group:
            dates_group.append(i[0])
    # 对同一组时间的所有评论进行合并
    fathion_words = []
    for i in dates_group:
        temp_words = ""
        for j in comments:
            if i == j[0]:
                temp_words += j[1]
        fathion_words.append(count_words(temp_words))  # 分词并获得前n个词
    screen_fathion_words = screen(fathion_words)  # 对分词结果进行筛选
    # 把结果写进json文件
    write_injson(dates_group, screen_fathion_words)
    write_incsv(dates_group, screen_fathion_words)
