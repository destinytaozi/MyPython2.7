# -*- coding: cp936 -*-
import MySQLdb
db=MySQLdb.connect('192.168.1.206','root','qazWSX098','00_oms')
cursor=db.cursor()
sql="select * from t_bill_sale_order where id = 20"
try:
    #执行sql
    cursor.execute(sql)
    #获取所有记录
    results=cursor.fetchall()
    print type(results)
    '''for row in results:
        id=row[0]
        cid=row[1]
        billno=row[2]
        print "id=%d,cid=%d,billno=%s"%(id,cid,billno)'''
        
except:
    print "Error:unable to fetch data"
db.close()
