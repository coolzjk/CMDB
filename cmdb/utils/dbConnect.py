#/usr/bin/env python
#-*- coding: utf-8 -*-
import pymysql
class dbConnect():
    def DatabaseLogin():
        db = pymysql.connect(host = '10.10.1.182', port = 3306, user = 'root', passwd = 'mysql', db = 'cmdb', charset="utf8")
        return db
def dbconnect(query):
    db = dbConnect.DatabaseLogin()
    cursor = db.cursor()
    serverinfo = '''select * from cmdb_server SERVER where CONCAT(IFNULL(SERVER.hostname,''),IFNULL(SERVER.sn,''),IFNULL(SERVER.model,''),IFNULL(SERVER.os_version,''),IFNULL(SERVER.manage_ip,'')) like '%%%s%%';'''%(query)
    cursor.execute(serverinfo)
    values = cursor.fetchall()
    cursor.close()
    return values
