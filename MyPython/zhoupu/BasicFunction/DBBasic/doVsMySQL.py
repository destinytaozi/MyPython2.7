# coding=utf-8
# This file named doVsOracle.py
# His duty is to do some interactive with Oracle
import MySQLdb

class doVsMySQL():
     def __init__(self):
         pass

     def connectMySQL(self,url,usrName,password,dbBase):
         conn = MySQLdb.connect(url,usrName,password,dbBase)
         return conn

     def getCursor(self,connect):
         cursor = connect.cursor()
         return cursor

     def selectMySQL(self,cursor,sql):
         cursor.execute(sql)
         result = cursor.fetchall()
         return result

     def closeMySQL(self,connect):
         connect.close()


