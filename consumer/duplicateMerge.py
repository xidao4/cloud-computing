from functools import reduce


def mergeDuplicate():
    f = open("./statis.csv", 'r+', encoding='utf-8')
    fNew = open("./mergeDuplicate.csv", 'w+', encoding='utf-8')
    fLine = f.readline()
    lines = f.readlines()
    items = []
    superDict = {}
    for line in lines:
        item = line.split(',')
        items.append(item)
    for item in items:
        if item[2] == "value":
            continue
        myKey = item[0]+"," + item[3][:len(item[3])]
        value = int(item[2])
        if myKey in superDict:
            superDict[myKey] += value
        else:
            superDict[myKey] = value
    keyList = superDict.keys()
    fNew.write(fLine)
    for key in keyList:
        value = superDict[key]
        nameAndDate = key.split(',')
        newStr = nameAndDate[0] + "," + "Chinese," + str(value) + "," + nameAndDate[1]
        fNew.write(newStr)
    f.close()



if __name__ == '__main__':
    mergeDuplicate()
