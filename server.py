# -*- coding:utf-8 -*-
from __future__ import print_function
 
import sys
 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json
from kafka import KafkaProducer
import time

if __name__ == "__main__":
    #consumer2.py
    sc = SparkContext(appName="PythonStreamingKafkaTest")
    ssc = StreamingContext(sc, 2)
 
    zkQuorum="localhost:2181"
    topic="test241"
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})

    #spark streaming处理

    kvs.pprint()

    ssc.start()
   
    #producer.py
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
        #爬虫所得数据
    time.sleep(2)
    for i in range(6):
        msg = "msg%d" % i
        ack=producer.send('test241', {msg: msg})
        metadata=ack.get()
        print(metadata.topic,metadata.partition,msg)
        time.sleep(1)

    producer.close()

    #consumer2.py
    ssc.awaitTermination()
