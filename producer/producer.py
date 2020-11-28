# -*- coding:utf-8 -*-

# 运行在python 3.8.1版本
import json
from kafka import KafkaProducer
import time
import bilibili_api
from spider.customizedAPI import get_comments
from spider.bilibiliSeries import getTodayDanmaku
from spider.textDealWith import get_all_statis

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
while True:
    timestamp = time.time()
    with open("timestampRecord", 'w') as timestampFile:
        lastTimestamp = timestampFile.read()
    #距离上一次执行程序已过两分钟
    if timestamp - lastTimestamp >= 120:
        with open("timestampRecord", 'w') as timestampFile:
            timestampFile.write(str(timestamp))
        comment = get_comments(timestamp=lastTimestamp)
        danmaku = getTodayDanmaku(timestamp=lastTimestamp)
        for i in range(0, len(comment)):
            ack=producer.send('bangumi', comment[i])
            metadata=ack.get()
            print(metadata.topic, metadata.partition)
        for i in range(0, len(danmaku))
            ack = producer.send('bangumi', comment[i])
            metadata = ack.get()
            print(metadata.topic, metadata.partition)

    else:
        time.sleep(1)
#此处for循环替换为爬虫代码

producer.close()
