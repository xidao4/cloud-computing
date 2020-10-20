from bilibili_api import bangumi
import json
import socket
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

if __name__=="__main__":
    result=[]
    with open("Oct_series.json","r") as oct_series_json:
        items=json.load(oct_series_json)

    number=0
    for item in items:
        seriesMap={}
        kafkaMap={}
        seriesMap["media_id"]=item["media_id"]#番剧季度id
        seriesMap["season_id"]=item["season_id"]#番剧季度id
        seriesMap["name"]=item["name"]#番剧名称
        seriesMap["url"]=item["url"]#url
        seriesMap["series_follow"]=bangumi.get_interact_data(item["season_id"])["series_follow"]#系列追番人数
        kafkaMap["series_follow"]=bangumi.get_interact_data(item["season_id"])["series_follow"]
        seriesMap["views"]=bangumi.get_collective_info(item["season_id"])["stat"]["views"]#总播放量
        kafkaMap["views"]=bangumi.get_collective_info(item["season_id"])["stat"]["views"]
        seriesMap["coins"] = bangumi.get_collective_info(item["season_id"])["stat"]["coins"]#投币数
        kafkaMap["coins"] = bangumi.get_collective_info(item["season_id"])["stat"]["coins"]
        seriesMap["danmakus"] = bangumi.get_collective_info(item["season_id"])["stat"]["danmakus"]#总弹幕数量
        kafkaMap["danmakus"] = bangumi.get_collective_info(item["season_id"])["stat"]["danmakus"]
        seriesMap["share"] = bangumi.get_collective_info(item["season_id"])["stat"]["share"]#分享人数
        kafkaMap["share"] = bangumi.get_collective_info(item["season_id"])["stat"]["share"]
        seriesMap["favorites"] = bangumi.get_collective_info(item["season_id"])["stat"]["favorites"]#收藏人数
        kafkaMap["favorites"] = bangumi.get_collective_info(item["season_id"])["stat"]["favorites"]
        number+=1
        result.append(seriesMap)
        print(kafkaMap)
        socket_client(str(kafkaMap))
    #json_str=json.dumps(result,ensure_ascii=False,indent=4)
    #with open("data.json",'w') as json_file:
    #    json_file.write(json_str)

