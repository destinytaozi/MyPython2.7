# -*- coding: UTF-8 -*-
import MySQLdb
#打开数据库连接
db=MySQLdb.connect('192.168.1.206','root','qazWSX098','TESTDB')
#使用cursor()获取操作游标
cursor=db.cursor()
#sql查询语句
sql='select * from employee where income > "%d"'%(1000)
try:
    #执行sql语句
    cursor.execute(sql)
    #获取所有记录列表
    results=cursor.fetchall()
    print results
except:
    print "Error:Unable to fetch data"

#关闭数据库连接
db.close()
