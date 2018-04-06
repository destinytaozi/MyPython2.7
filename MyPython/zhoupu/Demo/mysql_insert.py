# -*- coding: cp936 -*-
import MySQLdb
db = MySQLdb.connect('192.168.1.206','root','qazWSX098','TESTDB')
cursor=db.cursor()
cursor.execute('alter table employee modify sex varchar(4) comment "性别"')
sql="""
insert into employee values('Mac','Mohan',20,'M',2000)
"""
cursor.execute(sql)
db.commit()
db.close
