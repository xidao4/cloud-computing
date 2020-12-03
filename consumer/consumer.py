# 运行在python 3.5.2版本
# 要在机房配好的环境中

from __future__ import print_function
 

 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import csv

time_now='2020-11-20'
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


# 传入consumer的消息中文会显示为unicode编码，需要转化为utf-8编码才能正常显示
def decode(k):
    
     # strs=k['comment']
   #  strs.encode('utf-8').decode('unicode_escape')
     # k['comment']=strs+2
     temp_dic=eval(k)
     string=temp_dic['comment']
     string.encode('utf-8').decode('unicode_escape') #转码
     temp_dic['comment']=string
     return temp_dic


def writeRDD(rdd):
     global time_now
     csvFile = open(csv_out_path, "a+")  # 创建csv文件
     writer = csv.writer(csvFile)  # 创建写的对象
     source=rdd.collect()
     contents=[]
     for i in source:
          line=[]
          temp_str=i[0]
          line.append(names[ord(temp_str[8])-65][0])
          line.append('Chinese')
          line.append(i[1])
          line.append(temp_str[15:25])
          time_now=line[3]
          contents.append(line)
     for i in contents:
        writer.writerow(i)
        for j in current_popular:
             if j['name']== i[0]:
               #    print("HHHHHHHHHHHHHHHHHHHHHHHH",type(j['popular'])," and ", type(i[2]))
                  j['popular']+=i[2]
     csvFile.close()

     # print("写进csv完成")
     print(rdd.collect())
     current_contents=[['name', 'type','value','date']]
     for k in current_popular:
          temp=[]
          temp.append(k['name'])
          temp.append('Chinese')
          temp.append(k['popular'])
          temp.append(time_now)
          current_contents.append(temp)
     
     csvFile = open(current_out_path, "w")  # 创建csv文件
     writer = csv.writer(csvFile)  # 创建写的对象
     # 写入多行用writerows                                #写入多行
     writer.writerows(current_contents)
     csvFile.close()
     # print(current_popular)
     

def cut(rd):
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
     names=get_names(name_path)

     # f = open('current.csv','r')
     # reader = csv.reader(f)
     # rows  = [row for row in reader]
     # checkpt=[]
     # for row in rows:
     #      checkpt.append(row[2])
     #      # print("--------------",type(row))
     #      # print(row)
     # index = 1
     for i in names:
          temp_name=i[0]
          temp_dict={'name': temp_name, 'popular': 0} #str(checkpt[index])
          # index += 1
          current_popular.append(temp_dict)
     
     
     sc = SparkContext(appName="PythonStreamingKafkaTest")
     ssc = StreamingContext(sc, 1)
     
     zkQuorum = "localhost:2181"
     topic = "test"

     kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic:1}) #kafka为来源的Dstream构造
    
     temp_kvs= kvs.map(lambda x: x[1]) #用kafka producer 发送的消息内容重新构造Dstream
     divided_kvs=temp_kvs.map(decode) #kafka_producer 发送的中文内容在consumer处接受到时为unicode编码，需要转换为utf8编码
     sec_kvs=divided_kvs.flatMap(cut) #使用cut函数对评论进行解析拆分，rdd重构为一个由角色对应编号和弹幕/评论发送日期组成的字符串
     thir_kvs=sec_kvs.map(lambda word: (word, 1)) #将rdd构造为一个键值对，为reduceByKey做词频统计做准备
     four_kvs=thir_kvs.reduceByKey(lambda a, b: a+b) #将拥有相同键的rdd合并，做词频统计
     four_kvs.foreachRDD(lambda x: writeRDD(x)) #将统计结果写入文件
     
    


     # kvs.pprint()
     print("deg")
     ssc.start()
     ssc.awaitTermination()
