from bilibili_api import bangumi
import json


def getDetails(fanDic):#传入番剧的字典，内包含media_id,season_id信息
    return  0

if __name__=="__main__":
    result=[]
    with open("Oct_series.json","r") as oct_series_json:
        items=json.load(oct_series_json)

    number=0
    for item in items:
        seriesMap={}
        seriesMap["media_id"]=item["media_id"]#番剧季度id
        seriesMap["season_id"]=item["season_id"]#番剧季度id
        seriesMap["name"]=item["name"]#番剧名称
        seriesMap["url"]=item["url"]#url
        seriesMap["series_follow"]=bangumi.get_interact_data(item["season_id"])["series_follow"]#系列追番人数
        seriesMap["views"]=bangumi.get_collective_info(item["season_id"])["stat"]["views"]#总播放量
        seriesMap["coins"] = bangumi.get_collective_info(item["season_id"])["stat"]["coins"]#投币数
        seriesMap["danmakus"] = bangumi.get_collective_info(item["season_id"])["stat"]["danmakus"]#总弹幕数量
        seriesMap["share"] = bangumi.get_collective_info(item["season_id"])["stat"]["share"]#分享人数
        seriesMap["favorites"] = bangumi.get_collective_info(item["season_id"])["stat"]["favorites"]#收藏人数
        number+=1
        result.append(seriesMap)

    #json_str=json.dumps(result,ensure_ascii=False,indent=4)
    #with open("data.json",'w') as json_file:
    #    json_file.write(json_str)

