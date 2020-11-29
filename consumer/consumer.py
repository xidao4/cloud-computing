# 运行在python 3.5.2版本
# 要在机房配好的环境中

from __future__ import print_function
 
import sys
 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import csv

name_path='./names.txt'
csv_out_path='./statis.csv'
current_out_path='./current.csv'
names=[]
current_popular=[]
def get_names(path):  # 读取txt文件获取角色名字
    name = []
    with open(path, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            name.append(line.split(" "))
    return name

 #zhongwenluanmajiejue
def decode(k):
    
     # strs=k['comment']
   #  strs.encode('utf-8').decode('unicode_escape')
     # k['comment']=strs+2
    # print("debug")
     temp_dic=eval(k)
     string=temp_dic['comment']
     string.encode('utf-8').decode('unicode_escape')
     temp_dic['comment']=string
     # print(temp_dic['date'])
     # print(temp_dic['comment'])
     return temp_dic

def Myprint(rdd):
     csvFile = open(csv_out_path, "a+")  # 创建csv文件
     writer = csv.writer(csvFile)  # 创建写的对象
     source=rdd.collect()
     contents=[]
     for i in source:
          line=[]
          temp_str=i[0]
          line.append(names[ord(temp_str[8])-65][0])
          line.append(temp_str[15:25])
          line.append(i[1])
          contents.append(line)
     for i in contents:
        writer.writerow(i)
        for j in current_popular:
             if j['name']== i[0]:
                  j['popular']+=i[2]
     csvFile.close()

     # print("写进csv完成")
     print(rdd.collect())
     current_contents=[['名字','频数']]
     for k in current_popular:
          temp=[]
          temp.append(k['name'])
          temp.append(k['popular'])
          current_contents.append(temp)
     
     csvFile = open(current_out_path, "w")  # 创建csv文件
     writer = csv.writer(csvFile)  # 创建写的对象
     # 写入多行用writerows                                #写入多行
     writer.writerows(current_contents)
     csvFile.close()
     # print(current_popular)
     

def cut(rd):
     # print("cut")
     comm=rd['comment']
     counts=[]
     for i in names:
          count=0
          for j in i:
               count+=comm.count(j)
               if comm.count(j) > 0:
                    ano_comm=comm.replace(j,'')
                    comm=ano_comm
          counts.append(count)
     numb=[chr(i) for i in range(65, 65+len(names))]
     results=[]
     for i in range(0,len(numb)):
          j=counts[i]
          for k in range(0,j):
               temp="{"+"number"+":"+numb[i]+","+"date"+":"+rd['date']+"}"
               results.append(temp)

     return results


if __name__ == "__main__":
     # if len(sys.argv) != 3:
     #     print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
     #     exit(-1)


     names=get_names(name_path)
     print(names)
     for i in names:
          temp_name=i[0]
          temp_dict={'name':temp_name,'popular':0}
          current_popular.append(temp_dict)

     
     sc = SparkContext(appName="PythonStreamingKafkaTest")
     ssc = StreamingContext(sc, 1)
     
     zkQuorum = "localhost:2181"
     topic = "test"
     print("qq")
     kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic:1})
    
     temp_kvs= kvs.map(lambda x: x[1])
     divided_kvs=temp_kvs.map(decode)
     sec_kvs=divided_kvs.flatMap(cut)
     thir_kvs=sec_kvs.map(lambda word: (word,1))
     four_kvs=thir_kvs.reduceByKey(lambda a, b: a+b)
     four_kvs.foreachRDD(lambda x: Myprint(x))
     
    

     #sec_kvs.foreachRDD(lambda x: Myprint(x))

     # kvs.pprint()
     print("deg")
     ssc.start()
     ssc.awaitTermination()