# 运行在python 3.5.2版本
# 要在机房配好的环境中

from __future__ import print_function
 
import sys
 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
 
if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
    #     exit(-1)
 
    sc = SparkContext(appName="PythonStreamingKafkaTest")
    ssc = StreamingContext(sc, 1)
 
    zkQuorum="localhost:2181"
    topic="test"
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    
    kvs.pprint()

    ssc.start()
    ssc.awaitTermination()