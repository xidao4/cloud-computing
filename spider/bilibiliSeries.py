from bilibili_api import bangumi
from bilibili_api import common
from bilibili_api import bvid2aid
from bilibili_api import Verify
from spider.customizedAPI import get_comments, get_danmaku
from spider.textDealWith import get_all_statis
import bilibili_api
import json
import datetime
import time



def getDetails(fanDic):#传入番剧的字典，内包含media_id,season_id信息
    return  0


def getTodayDanmaku(season_id = 34430, timeLimit = 0):
    verify = Verify(sessdata="c9f59cdb%2C1609146929%2C7963a*71", csrf="b6ce9e789575330a9308fad04b56377a")
    bg = bangumi.get_collective_info(seasonId)
    res = []
    for i in range(0, len(bg["episodes"])):
        bgAid = bvid2aid(bg["episodes"][i]["bvid"])
        Danmaku = bilibili_api.video.get_danmaku(aid=bgAid, verify=verify,timeLimit=timeLimit)
        res += Danmaku  # 添加弹幕
        print("已爬弹幕数： " + str(len(res)))
        time.sleep(1)
    return res


def getAllComments(season_id = 34430, timeLimit = 0):
    bg = bangumi.get_collective_info(seasonId)
    res = []
    for i in range(0, len(bg["episodes"])):
        bgAid = bvid2aid(bg["episodes"][i]["bvid"])
        res += get_comments(oid=bgAid, type_="video", timeLimit=timeLimit)  # 添加评论
        print("已爬评论数： " + str(len(res)))
        time.sleep(1)
    return res





if __name__ == "__main__":
    seasonId = 34430
    res1 = getTodayDanmaku(timeLimit=1606553289)
    res2 =getAllComments(timeLimit=1606553289)
    res = get_all_statis(res1, res2)
    print(1)
    # result=[]
    # verify = Verify(sessdata= "c9f59cdb%2C1609146929%2C7963a*71", csrf = "b6ce9e789575330a9308fad04b56377a")
    # with open("Oct_series.json", "r") as oct_series_json:
    #     items=json.load(oct_series_json)
    # bilibili_api.request_settings["proxies"]={}
    #
    # for item in items:
    #     if item["media_id"] == 28229899:
    #         seriesMap={}
    #         kafkaMap={'danmaku':[], 'comment':[]}
    #         seriesMap["media_id"] = item["media_id"]#番剧季度id
    #         seriesMap["season_id"] = item["season_id"]#番剧季度id
    #         seriesMap["name"] = item["name"]#番剧名称
    #         seriesMap["url"] = item["url"]#url
    #         seriesMap["series_follow"] = bangumi.get_interact_data(item["season_id"])["series_follow"]#系列追番人数
    #         kafkaMap["series_follow"] = seriesMap["series_follow"]
    #         test = bangumi.get_collective_info(item["season_id"])
    #         for i in range(0, len(test["episodes"])):
    #             testAid = bvid2aid(test["episodes"][i]["bvid"])
    #             monthIndex = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
    #             danmakuIndex = bilibili_api.video.get_history_danmaku_index(aid=testAid, verify=verify, date=monthIndex ) #有的集数十月份并没有弹幕
    #             if danmakuIndex is None:
    #                 danmakuIndex = []
    #             danmakuIndex += bilibili_api.video.get_history_danmaku_index(aid=testAid, verify=verify)
    #             for j in range(0, len(danmakuIndex)):
    #                 dateTime = datetime.datetime.strptime(danmakuIndex[j], "%Y-%m-%d")
    #                 Danmaku = bilibili_api.video.get_danmaku(aid=testAid, date=dateTime, verify=verify, timeLimit=1606552825)
    #                 kafkaMap['danmaku'] += Danmaku #添加弹幕
    #                 print("已爬弹幕数： " + str(len(kafkaMap['danmaku'])))
    #                 time.sleep(1)
    #             testComments = get_comments(oid=testAid, type_="video", timeLimit=1606552825)
    #             kafkaMap['comment'] += testComments #添加单集评论
    #         json_BangumiComments = json.dumps(kafkaMap['comment'], ensure_ascii=False, indent=4)
    #         json_BangumiDanmaku = json.dumps(kafkaMap['danmaku'], ensure_ascii=False, indent=4)
    #         with open("BangumiComment.json", 'w', encoding='utf-8') as json_CommentFile:
    #             json_CommentFile.write(json_BangumiComments)
    #         with open("BangumiDanmaku.json", 'w', encoding='utf-8') as json_Danmakufile:
    #             json_Danmakufile.write(json_BangumiDanmaku)
    #
    #
    # LOLBvidLists = ["BV1my4y1k7m1", "BV1ri4y1E7Zg", "BV1B54y1k7cL", "BV1Yh41197Ho", "BV1dT4y1c76Q", "BV1U5411j77H", "BV1y54y1k7tz",
    #                "BV15a4y1L7zo", "BV1KK411A7b1", "BV1ft4y1v7TF", "BV1tV41127ne", "BV15p4y1k7Fg", "BV1bK4y177v4", "BV15r4y1w7T5",
    #                "BV1dv411k7xd", "BV1vz4y1C7cv", "BV1QK4y177Lq", "BV1iK411A733", "BV1WK4y1E7ex", "BV1nV41117b3",
    #                "BV1Pp4y1z7Qc"
    #                ]
    # LOLBvid = "BV1D54y1z7bv"
    # LOLComments = []
    # for Bvid in LOLBvidLists:
    #     LOLAvid = bvid2aid(Bvid)
    #     LOLComments += get_comments(oid=LOLAvid, type_="video")
    # json_Comment = json.dumps(LOLComments, ensure_ascii=False, indent=4)
    # with open("LOLcomment.json", 'w', encoding='utf-8') as json_file:
    #     json_file.write(json_Comment)
    # print(kafkaMap)
    # socket_client(str(kafkaMap))

    #json_str=json.dumps(result,ensure_ascii=False,indent=4)
    #with open("data.json",'w') as json_file:
    #    json_file.write(json_str)


