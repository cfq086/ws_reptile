import urllib.request
import urllib.parse
import json
import gzip
import time
import re
import tomd

import os


def open_url(url):
    '''打开链接，并返回源代码'''
    header = {
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        "X - Requested - With": "XMLHttpRequest",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4",
        "Cookie": "wxuin=1430203230; devicetype=android-26; version=27000435; lang=zh_CN; pass_ticket=OhyXG1sgdzBGx4Q9alQQ3XjNwwkvO7dFuV9m4q3HNwJsMutPCEcjj8JBiGqFug6; wap_sid2=CN7W/KkFElxlTzBaVFdQS2h5Q05JYkdzMm94dWJDV1JnNWdvaTFVSnEzX0FXTk9FU3k0WHdUakppcW84Snd1MHRoaGJOYXRfZ1dUUzVJSDNNVGpCMmhia3NsTHpReGdFQUFBfjC/iKDyBTgNQJVO"
    }

    req = urllib.request.Request(url, headers=header)
    request = urllib.request.urlopen(req)

    res = request.read()

    print("【是否启动gzip压缩】：", request.headers["Content-Encoding"])
    if request.headers["Content-Encoding"] == "gzip":
        html = gzip.decompress(res).decode("utf-8")
    else:
        html = res.decode("utf-8")
    return html


def pj_url(offset="0"):
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI5Mzk4MjYzOA==&f=json&"
    data = {
        "offset": "0",
        "count": "10",
        "is_ok": "1",
        "scene": "124",
        "key": "6b57f9ad7659ff1fe1fde7da4d50ac54157841d8208ad46259397558a09e76904f2ba878f92a0c83c1b7856d42f51067391aa56e809897bd3930aa4d2720d75fc3b813c832c4282f774e1003524b5d03"}
    parm = "&uin=MTQzMDIwMzIzMA%3D%3D&pass_ticket=IznpBAYsYWaJF9Y8rs%2FQJP034V101b1h9F9yWnlO2u1HN9H2bup9e2B9h5RZgXwT"
    data["offset"] = offset
    new_data = urllib.parse.urlencode(data)
    pj = url + new_data + parm
    return pj


def get_josn(html):
    jsons = json.loads(html)

    if not jsons["ret"]:
        print("加载成功：", jsons["ret"], jsons["errmsg"])
        html = html.replace('"general_msg_list":"', '"general_msg_list":')
        html = html.replace('","next_offset"', ',"next_offset"')
        html = html.replace('\\', '')
        return 1, json.loads(html)
    else:
        print("出错:", jsons["ret"], jsons["errmsg"])
        return 0, jsons


def get_pags(json):
    vas = json["general_msg_list"]["list"]
    for itm in vas:

        content_url = itm["app_msg_ext_info"]["content_url"]
        cover = itm["app_msg_ext_info"]["cover"]
        timeArray = time.localtime(datatime)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        filename = validateTitle(title)
        #
        # print("\n***************\n")
        # print(filename, " 文章保存")
        # # print("文章id：", id)
        # # print("时间戳：%s,时间：%s" % (datatime, otherStyleTime))
        # # print("文章标题：", title)
        # # print("链接：", content_url)
        # # print("缩略图：", cover)
        # 保存页面
        # save_page(content_url, filename)
    print("当前页保存完成")


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)
    return new_title


def save_page(url, filename):
    html = open_url(url)
    print("保存成网页：")
    with open(filename + ".html", "w", encoding="utf-8") as f:
        f.write(html)

    print("保存成md：")

    md = tomd.Tomd(html).markdown
    with open(filename + ".md", "w", encoding="utf-8") as f:
        f.write(md)


def save_mysql(jsons,a):
    vas = jsons["general_msg_list"]["list"]
    for itm in vas:
        id = itm["comm_msg_info"]["id"]
        type = itm["comm_msg_info"]["type"]
        datatime = itm["comm_msg_info"]["datetime"]
        fakeid = itm["comm_msg_info"]["fakeid"]
        status = itm["comm_msg_info"]["status"]
        title = itm["app_msg_ext_info"]["title"]
        author= itm["app_msg_ext_info"]["author"]
        content_url=itm["app_msg_ext_info"]["content_url"]
        cover = itm["app_msg_ext_info"]["cover"]
        copyright_stat = itm["app_msg_ext_info"]["copyright_stat"]

        a.install_msg(sid=id, stype=type, sdatatime=datatime, sfakeid=fakeid, sstatus=status)
        a.install_ext(sid=id, stitle=title, sauthor=author, scontent_url=content_url,scover=cover,scopyright_stat=copyright_stat)
