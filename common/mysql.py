import pymysql


class Mysql:
    def connect_mysql(self, mysql):
        # 连接数据库从表里获取信息
        db = pymysql.connect(host='192.168.1.13', user='root', password='uENQfwm2kiTBkyhQ', db='mars_test',
                             port=3306)
        cur = db.cursor()
        # 查询我的手机所有验证码按照降序排列
        cur.execute(mysql)
        # 返回第一条数据
        results = cur.fetchone()
        cur.close()
        db.close()
        return results

