# -*- coding:utf-8 -*-

# 运行在python 3.8.1版本
import json
from kafka import KafkaProducer
import time
from spider import bilibili_api
from spider.customizedAPI import get_comments
from spider.bilibiliSeries import getTodayDanmaku
from spider.bilibiliSeries import getAllComments
from spider.textDealWith import get_all_statis

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
while True:
    timestamp = int(time.time())
    with open("timestampRecord", 'r') as f:
    #with open("C:\\Users\\12736\\Desktop\\学习\\云计算\\groupProject\\cloud-computing\\producer\\timestampRecord", 'r') as f:
        lastTimestamp = int(f.readline())
    #距离上一次执行程序已过两分钟
    if timestamp - int(lastTimestamp) >= 120:
        with open("timestampRecord", 'w+') as timestampFile:
            timestampFile.write(str(timestamp))
        comment = getAllComments(timeLimit=lastTimestamp)
        danmaku = getTodayDanmaku(timeLimit=lastTimestamp)
        print(1)
        for i in range(0, len(comment)):
            ack=producer.send('bangumi', comment[i]['content'])
            metadata=ack.get()
            print(metadata.topic, metadata.partition)
        for i in range(0, len(danmaku)):
            ack = producer.send('bangumi', danmaku[i]['content'])
            metadata = ack.get()
            print(metadata.topic, metadata.partition)

    else:
        time.sleep(1)
#此处for循环替换为爬虫代码

producer.close()
