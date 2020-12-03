# -*- coding: UTF-8 -*-
# 处理番剧
import json
import collections  # 计算词频
import datetime
import time
import csv


def read_json1(path):  # 读取json文件，带时间戳
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


def read_json2(path):  # 读取文件，时间是标准时间
    barr = []
    with open(path, 'r', encoding='UTF-8') as f:  # 读取数据源
        data = json.load(f)
    # 读进一个二维数组里
    for dict1 in data:
        temp = []
        for value in dict1.values():
            temp.append(value)
        barr.append(temp[0:2])  # 最后一个时间不要
    for ba in barr:
        temp_time = ba[0][0:10]
        week = (int(temp_time[-2]) * 10 + int(temp_time[-1])) // 7 + 1
        if week > 4:
            week = 4
        ba[0] = temp_time[0:-2] + str(0) + str(week)
    return barr


def get_names(path):  # 读取txt文件获取角色名字
    name = []
    with open(path, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            name.append(line.split(" "))
    return name


def statis(dates, texts):  # 统计个数
    firstLine = ["名字", "时间", "频数"]
    contents = [firstLine]
    for m in range(0, len(dates_group)):
        t = merged_text[m]
        for n in names:
            count = 0
            for k in n:
                count += t.count(k)
            contents.append([n[0], dates_group[m], count])
    return contents  # 返回值直接写进csv就行


def write_incsv(contents):  # 写进csv
    csvFile = open(csv_out_path, "w")  # 创建csv文件
    writer = csv.writer(csvFile)  # 创建写的对象
    # 写入多行用writerows                                #写入多行
    writer.writerows(contents)
    csvFile.close()
    print("写进csv完成")


def get_all_statis(list1, list2):   #读取名字是直接从名字的txt里面读取的
    source_path_names = 'names.txt'
    texts = ""
    for dic in list1:
        values = list(dic.values())
        texts += values[1]
    for dic in list2:
        values = list(dic.values())
        texts += values[1]
    people_name = get_names(source_path_names)
    counts = []
    for n in people_name:
        count = 0
        for k in n:
            count += texts.count(k)
        counts.append(count)
    return dict(zip([x[0] for x in people_name], counts))


if __name__ == '__main__':
    source_path_comment = 'BangumiComment.json'
    source_path_barrage = 'BangumiDanmaku.json'
    source_path_names = 'names.txt'
    csv_out_path = 'anime_top_people.csv'
    comments = read_json1(source_path_comment)
    barrages = read_json2(source_path_barrage)
    names = get_names(source_path_names)
    all_text = comments + barrages  # 评论和弹幕合并成一个数组

    # 对时间进行去重分组，一个月分四组
    dates_group = []
    for i in all_text:
        if i[0] not in dates_group:
            dates_group.append(i[0])
    # 对同一组时间的所有内容进行合并
    merged_text = []
    for i in dates_group:
        temp_text = ""
        for j in all_text:
            if i == j[0]:
                temp_text += j[1]
        merged_text.append(temp_text)

    content_to_write = statis(dates_group, merged_text)
    write_incsv(content_to_write)
