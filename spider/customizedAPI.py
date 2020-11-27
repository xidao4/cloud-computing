import bilibili_api
import time
import datetime
import requests
from xml.dom.minidom import parseString
import json

API = bilibili_api.utils.get_api()

COMMENT_TYPE_MAP = {
    "video": 1,
    "article": 12,
    "dynamic_draw": 11,
    "dynamic_text": 17,
    "audio": 14,
    "audio_list": 19
}
COMMENT_SORT_MAP = {
    "like": 2,
    "time": 0
}


def get_comments_raw(oid: int, type_: str, order: str = "time", pn: int = 1, verify: bilibili_api.utils.Verify = None):
    """
    通用获取评论
    :param oid:
    :param type_:
    :param order:
    :param pn:
    :param verify:
    :return:
    """
    if verify is None:
        verify = bilibili_api.utils.Verify()

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, bilibili_api.exceptions.BilibiliApiException("不支持的评论类型")

    order = COMMENT_SORT_MAP.get(order, None)
    assert order is not None, bilibili_api.exceptions.BilibiliApiException("不支持的排序方式，支持：time（时间倒序），like（热度倒序）")
    # 参数检查完毕
    params = {
        "oid": oid,
        "type": type_,
        "sort": order,
        "pn": pn
    }
    comment_api = API["common"]["comment"]
    api = comment_api.get("get", None)
    resp = bilibili_api.utils.get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_comments(oid: int, type_: str, order: str = "time",
                 limit: int = 1919810, callback=None, verify: bilibili_api.utils.Verify = None):
    """
    通用循环获取评论
    :param type_:
    :param order:
    :param callback: 回调函数
    :param oid:
    :param limit: 限制数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = bilibili_api.utils.Verify()

    count = 0
    replies = []
    page = 1
    while count < limit:
        resp = get_comments_raw(oid=oid, pn=page, order=order, verify=verify, type_=type_)
        if "replies" not in resp:
            break
        if resp["replies"] is None:
            break
        count += len(resp["replies"])
        for comment in resp["replies"]:
            dict = {'ctime': comment['ctime'], 'content': comment['content']['message']}
            replies.append(dict)
        # replies += resp["replies"]
        if callable(callback):
            callback(resp["replies"])
        page += 1
        time.sleep(5) #等待五秒再发起下一次api请求
    return replies[:limit]


def get_danmaku(bvid: str = None, aid: int = None, page: int = 0,
                verify: bilibili_api.Verify = None, date: datetime.date = None):
    """
    获取弹幕
    :param aid:
    :param bvid:
    :param page: 分p数
    :param verify: date不为None时需要SESSDATA验证
    :param date: 为None时获取最新弹幕，为datetime.date时获取历史弹幕
    """

    if not (aid or bvid):
        raise bilibili_api.exceptions.NoIdException
    if verify is None:
        verify = bilibili_api.Verify()
    if date is not None:
        if not verify.has_sess():
            raise bilibili_api.exceptions.NoPermissionException(bilibili_api.MESSAGES["no_sess"])
    api = API["video"]["info"]["danmaku"] if date is None else API["video"]["info"]["history_danmaku"]
    info = bilibili_api.video.get_video_info(aid=aid, bvid=bvid, verify=verify)
    page_id = info["pages"][page]["cid"]
    params = {
        "oid": page_id
    }
    if date is not None:
        params["date"] = date.strftime("%Y-%m-%d")
        params["type"] = 1
    req = requests.get(api["url"], params=params, headers=bilibili_api.DEFAULT_HEADERS, cookies=verify.get_cookies())
    if req.ok:
        con = req.content.decode("utf-8")
        try:
            xml = parseString(con)
        except Exception:
            j = json.loads(con)
            raise bilibili_api.exceptions.BilibiliException(j["code"], j["message"])
        danmaku = xml.getElementsByTagName("d")
        py_danmaku = []
        for d in danmaku:
            info = d.getAttribute("p").split(",")
            text = d.childNodes[0].data
            if info[5] == '0':
                is_sub = False
            else:
                is_sub = True
            dm = bilibili_api.Danmaku(
                dm_time=float(info[0]),
                send_time=int(info[4]),
                crc32_id=info[6],
                color=bilibili_api.Color(info[3]),
                mode=info[1],
                font_size=info[2],
                is_sub=is_sub,
                text=text
            )
            py_danmaku.append(dm)
        return py_danmaku
    else:
        raise bilibili_api.exceptions.NetworkException(req.status_code)