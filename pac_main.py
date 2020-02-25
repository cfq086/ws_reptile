from ws_reptile.pac_spirit import *
from ws_reptile.mysql_spirit import *

if not os.path.isdir("xxoo"):
    os.mkdir("xxoo")
os.chdir("xxoo")
zt = 1
i=1
url = pj_url()
conn = MYsqld(passwd="sjk520", db="pac")
while zt:
    print("第%d页！" % i)
    html = open_url(url)
    z, jsons = get_josn(html)
    if z:
        # get_pags(jsons)
        print("数据库")
        save_mysql(jsons, conn)
        if jsons["can_msg_continue"]:
            url = pj_url(jsons["msg_count"])
            inp = input("获取到下一页：【1：继续】【0：取消】回车默认：1")
            if inp == "0":
                zt = 0
        else:
            zt = 0
        i+=1
    else:
        print("获取失败", jsons)
        zt = 0
