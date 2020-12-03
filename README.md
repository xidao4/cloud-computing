# cloud-computing
2020年云计算大作业

在机房配好的环境中 运行步骤：
cc用户，密码666666,没有root用户

#### 1.

cd ~/kafka

./bin/zookeeper-server-start.sh config/zookeeper.properties

不要关闭terminal

#### 2.

新开一个terminal

bin/kafka-server-start.sh config/server.properties

也不要关闭

#### 3.

再开一个terminal

./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

可以关闭

#### 4.

项目位置 ~/spark/mycode/consumer和/producer

/usr/bin/python /home/cc/Desktop/cloud-computing-dev/producer/producer.py


打开VSCode，File>OpenFolder 选择consumer文件夹（左下角可看到解释器版本为3.5.2）

再打开一个VScode，打开producer文件夹 （左下角解释器版本3.8.1）

先跑consumer.py，consumer.py需要在consumer目录下打开控制台，再运行consumer.py文件
/usr/bin/python3 /home/xidao/cloud-computing/consumer/consumer.py
其中kvs = KafkaUtils.createStream得到spark streaming流，kvs.pprint()直接打印监听到的数据

再跑producer.py, producer.py需要在cloud-computing即项目根目录下打开控制台，再运行producer.py文件/usr/bin/python /home/xidao/cloud-computing/producer/producer.py
把for循环替换为爬虫代码，用KafkaProducer.send到本地Kafka环境的broker服务器上。

