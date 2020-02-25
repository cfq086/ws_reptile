import pymysql


class MYsqld():
    def __init__(self, host="localhost", port=3306, user="root", passwd="root", db="db", charset="utf8"):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cur = self.conn.cursor()

    def seletc(self, s):
        """数据库查询方法"""
        effect_row = self.cur.execute(s)
        if effect_row:
            print("MYsqld:查询到【%d】条数据" % effect_row)
            return self.cur.fetchall()  # 返回查询到的内容
        else:
            return 0

    def updata(self, s):
        effect_row = self.cur.execute(s)  # 受影响的条数
        self.conn.commit()  # 保存修改的内容。不然将不会保存
        if effect_row:
            print("MYsqld:【%d】条数据已修改！" % effect_row)

        else:
            print("MYsqld:没有修改任何数据")

    def install_msg(self, sid, stype, sdatatime, sfakeid, sstatus):
        effect_row=False
        sql = "INSERT INTO `msg_info` (`id`, `type`, `datetime`, `fakeid`, `status`) VALUES ('" + sid + "', '" + stype + "', '" + sdatatime + "', '" + sfakeid + "', '" + sstatus + "')"
        try:
            effect_row = self.cur.execute(sql)  # 如果插入失败则不返回内容，变量未被定义
            self.conn.commit()                  # 下面的语句块也不会被执行，
        except pymysql.err.IntegrityError as result:
            if result.args[0]==1062:
                print("msg表中id：【%s】的文章已存在" % str(result.args[1]).split("'")[1])
        except Exception as result:
            print(type(result))
            print(result.args[1])
            print("未知错误：%s"%result)
        finally:
            return effect_row


    def install_ext(self, sid, stitle, sauthor, scontent_url, scover, scopyright_stat):
        effect_row=False
        sql = "INSERT INTO `ext_info` (`id`, `title`, `author`, `content_url`, `cover`, `copyright_stat`) VALUES ('" + sid + "', '" + stitle + "', '" + sauthor + "', '" + scontent_url + "', '" + scover + "','" + scopyright_stat + "')"
        try:
            effect_row = self.cur.execute(sql)  # 如果插入失败则不返回内容，变量未被定义
            self.conn.commit()  # 下面的语句块也不会被执行，
        except pymysql.err.IntegrityError as result:
            if result.args[0] == 1062:
                print("ext表中id：【%s】的文章已存在" % str(result.args[1]).split("'")[1])
        except Exception as result:
            print("未知错误：%s"%result)
        return effect_row


    def delete(self, s):
        effect_row = self.cur.execute(s)
        self.conn.commit()
        if effect_row:
            print("MYsqld:【%d】条数据已删除" % effect_row)
        else:
            print("MYsqld:没有删除任何数据")

    def __del__(self):
        print("\nMYsqld: 关闭Mysql游标，关闭Mysql链接")
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    a = MYsqld(passwd="sjk520", db="pac")
    # e = a.seletc("select * from msg_info")
    # for i in e:
    #     print(i)
    id = "101001185"
    stype = "123"
    datatime = "123"
    fakeid = "123"
    status = "123"
    title = "1212"
    author = "1212"
    content_url = "1212"
    cover = "1212"
    copyright_stat = "1212"
    b=a.install_msg(sid=id, stype=stype, sdatatime=datatime, sfakeid=fakeid, sstatus=status)
    # a.install_ext(sid=id, stitle=title, sauthor=author, scontent_url=content_url,scover=cover,scopyright_stat=copyright_stat)
    print(b)
# pymysql.Connect()参数说明
# host(str):      MySQL服务器地址
# port(int):      MySQL服务器端口号
# user(str):      用户名
# passwd(str):    密码
# db(str):        数据库名称
# charset(str):   连接编码
#
# connection对象支持的方法
# cursor()        使用该连接创建并返回游标
# commit()        提交当前事务
# rollback()      回滚当前事务
# close()         关闭连接
#
# cursor对象支持的方法
# execute(op)     执行一个数据库的查询命令
# fetchone()      取得结果集的下一行
# fetchmany(size) 获取结果集的下几行
# fetchall()      获取结果集中的所有行
# rowcount()      返回数据条数或影响行数
# close()         关闭游标对象
