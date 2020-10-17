import re
import urllib.request , urllib.error,urllib.parse
from bilibili_api import bangumi
import json

# 得到指定一个URL的网页内容,得到番剧索引中的信息
def askURL(url):
    head={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    request=urllib.request.Request(url=url,headers=head)

    html=""
    try:
        response=urllib.request.urlopen(request)  # 接受返回的信息
        html=response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

# 爬取网页,爬取首页番剧索引的内容，得到所有新番信息fan_map
def getData(baseurl):
    dataList=[]
    # 逐一解析数据
    baseurl2 = "&season_type=1&pagesize=20&type=1"
    fan_number=0
    fan_map = []  # 新番基本信息，从首页番剧索引中爬取
    for i in range(0,2):
        url=baseurl+str(i+1)+baseurl2
        html=askURL(url)  # 保存获取到的网页源码
        data=json.loads(html)
        pat=re.compile(r'10(.*?)')
        for item in data["data"]["list"]:
            if pat.search(item["order"])!=None:
                new_map={}
                new_map["media_id"] = item["media_id"]
                new_map["season_id"] = item["season_id"]
                new_map["name"] = item["title"]
                new_map["url"] = item["link"]
                new_map["time"]=item["order"]
                fan_map.append(new_map)
                fan_number+=1
    return fan_map

def getDetails(fanDic):#传入番剧的字典，内包含media_id,season_id信息
    return  0



if __name__=="__main__":
    result=[]
    items=getData("https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=5&st=1&sort=0&page=")
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
    json_str=json.dumps(result,ensure_ascii=False,indent=4)
    with open("data.json",'w') as json_file:
        json_file.write(json_str)
