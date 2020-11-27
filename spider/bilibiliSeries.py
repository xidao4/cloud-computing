from bilibili_api import bangumi
from bilibili_api import common
from bilibili_api import bvid2aid
from bilibili_api import Verify
from customizedAPI import get_comments, get_danmaku
import bilibili_api
import json
import socket
import datetime
import time
SERVER_IP = 'localhost'
PORT=8081


# 将数据传给kafka的socket
def socket_client(data):
    # 创建tcp套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 链接服务器
    client_socket.connect((SERVER_IP, PORT))
    print(data)
    client_socket.send(data.encode("UTF-8"))
    client_socket.close()


def getDetails(fanDic):#传入番剧的字典，内包含media_id,season_id信息
    return  0


if __name__ == "__main__":
    result=[]
    verify = Verify(sessdata= "c9f59cdb%2C1609146929%2C7963a*71", csrf = "b6ce9e789575330a9308fad04b56377a")
    with open("Oct_series.json", "r") as oct_series_json:
        items=json.load(oct_series_json)
    bilibili_api.request_settings["proxies"]={}

    for item in items:
        if item["media_id"] == 28229899:
            seriesMap={}
            kafkaMap={'danmaku':[], 'comment':[]}
            seriesMap["media_id"] = item["media_id"]#番剧季度id
            seriesMap["season_id"] = item["season_id"]#番剧季度id
            seriesMap["name"] = item["name"]#番剧名称
            seriesMap["url"] = item["url"]#url
            seriesMap["series_follow"] = bangumi.get_interact_data(item["season_id"])["series_follow"]#系列追番人数
            kafkaMap["series_follow"] = seriesMap["series_follow"]
            test = bangumi.get_collective_info(item["season_id"])
            for i in range(0, len(test["episodes"])):
                testAid = bvid2aid(test["episodes"][i]["bvid"])
                monthIndex = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
                danmakuIndex = bilibili_api.video.get_history_danmaku_index(aid=testAid, verify=verify, date=monthIndex )
                danmakuIndex += bilibili_api.video.get_history_danmaku_index(aid=testAid, verify=verify)
                for j in range(0, len(danmakuIndex)):
                    dateTime = datetime.datetime.strptime(danmakuIndex[j], "%Y-%m-%d")
                    testDanmaku = bilibili_api.video.get_danmaku(aid=testAid, date=dateTime, verify=verify)
                    kafkaMap['danmaku'] += testDanmaku #添加弹幕
                    time.sleep(5)
                testComments = get_comments(oid=test, type_="video")
                kafkaMap['comment'] += testComments #添加单集评论

            # print(kafkaMap)
            # socket_client(str(kafkaMap))
    #json_str=json.dumps(result,ensure_ascii=False,indent=4)
    #with open("data.json",'w') as json_file:
    #    json_file.write(json_str)

