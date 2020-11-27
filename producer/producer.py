# -*- coding:utf-8 -*-

# 运行在python 3.8.1版本
import json
from kafka import KafkaProducer
import time


producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
for i in range(4):
    msg = "msg%d" % i
    ack=producer.send('test', {msg: msg})
    metadata=ack.get()
    print(metadata.topic,metadata.partition)
    time.sleep(1)
#此处for循环替换为爬虫代码

producer.close()
