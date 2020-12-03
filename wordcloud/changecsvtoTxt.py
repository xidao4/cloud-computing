# coding=utf-8
import csv
import pandas as pd


def change_txt(path1, path2):
    data = []
    csv_reader = csv.reader(open(path1))
    for row in csv_reader:
        temp = []
        if row[0] not in [x[0] for x in data]:

            temp.append(row[0])
            temp.append(row[2])
            data.append(temp)
    data=data[1:]
    for i in data:
        i[1]=int(i[1])
    with open(path2, "w",encoding='utf-8') as f:
        f.write(str(data))


if __name__ == '__main__':
    source_csv_path = 'anime_top_people.csv'
    out_txt_path = 'data.txt'
    change_txt(source_csv_path, out_txt_path)
