# -*- coding: utf-8 -*-
# This is the file "CheckSaleBill.py"
# We use it to check the sale bill
# coding=utf-8
# This file named doVsOracle.py
# His duty is to do some interactive with Oracle
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import MySQLdb

class checkSaleBill():
     def __init__(self):
         pass

     def connectMySQL(self,url,usrName,password,dbBase):
         conn = MySQLdb.connect(url,usrName,password,dbBase,charset="utf8")
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

     def queryAndClose(self,url,usrName,password,dbBase,sql):
         conn = self.connectMySQL(url,usrName,password,dbBase)
         cursor = self.getCursor(conn)
         result = self.selectMySQL(cursor,sql)
         self.closeMySQL(conn)
         return result

     def SaleOrderIsGenerate(self,sqlResult):
         global result
         for i in len(sqlResult):
             print sqlResult[i]
             if sqlResult[i]:
                result=sqlResult[i]
             else:
                result=sqlResult[i]
         return result

    def send_mail_2array(cls, SMTP_host, from_account, from_password, to_account, subject, content):
        # 1.实例化SMTP
        global msg_b, msg_all
        smtp = smtplib.SMTP()
        # 2. 链接邮件服务器
        smtp.connect(SMTP_host)
        # 3. 配置发送邮箱的用户名和密码
        smtp.login(from_account, from_password)
        # 4. 配置发送内容msg
        if type(content) == str:  # 如果content传参为一个字符串则返回这个字符串 否则（列表）则把列表数据传到html表中
            msg = MIMEText(content, 'HTML', 'utf-8')
        else:
            msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_account
        msg['To'] = ','.join(to_account)
        # 5. 配置发送邮箱，接收邮箱，以及发送内容
        smtp.sendmail(from_account, to_account, msg.as_string())
        # 6. 关闭邮件服务
        smtp.quit()

if __name__ == '__main__':
    cs=checkSaleBill()
    sqlSaleOrder = '''
        SELECT saleBillNo FROM t_bill_sale_order WHERE mpState=6;
    '''
    cs.queryAndClose('192.168.1.206','root','qazWSX098','saas_erp_965',sqlSaleOrder)

