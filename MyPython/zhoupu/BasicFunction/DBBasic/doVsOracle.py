# coding=utf-8
# This file named doVsOracle.py
# His duty is to do some interactive with Oracle
import cx_Oracle

class doVsOracle():
     def __init__(self):
         pass

     def connectOracle(self,usrName,password,url_sid):
         conn = cx_Oracle.connect(usrName,password,url_sid)
         cursor = conn.cursor()
         return cursor

     def selectSQL(self,cursor,sql):
         cursor.execute(sql)
         result = cursor.fetchall()
         return result



