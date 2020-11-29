import csv
name_path='./names.txt'
csv_out_path='./statis.csv'
names=[]
def get_names(path):  # 读取txt文件获取角色名字
    name = []
    with open(path, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            name.append(line.split(" "))
    return name


if __name__ == "__main__":
    source=[('{number:A,date:2012-01-14}', 8), ('{number:L,date:2012-01-14}', 12), ('{number:E,date:2012-01-14}', 8)]
    csvFile = open(csv_out_path, "a+")  # 创建csv文件
    writer = csv.writer(csvFile)  # 创建写的对象
    writer.writerow( ["名字", "时间", "频数"])
    names=get_names(name_path)
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
    csvFile.close()