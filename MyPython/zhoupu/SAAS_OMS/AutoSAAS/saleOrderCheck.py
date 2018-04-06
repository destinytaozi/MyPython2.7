# -*- coding: utf-8 -*-
# This is the file "saleOrderCheck.py"
# We use it to check the accounted sale order bill is function normal.
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from string import join

import MySQLdb
import datetime

class saleOrderCheck():
    @classmethod
    def connect_mysql_select(cls, database_url, database_user, database_password, database_name, sql):
        bill_info = []
        mysql_con = MySQLdb.connect(database_url, database_user, database_password, database_name,charset="utf8")  # 连接数据库
        cursor = mysql_con.cursor()  # 获取数据库操作游标 实例化mysql数据库
        try:
            cursor.execute(sql)  # 执行sql
            results = cursor.fetchall()  # 读取sql的所有结果
            if results:  # 判断如果查询结果不为空则给出具体返回值 否则给出字符串
                for row in results:  # 逐行遍历结果 并按列记录在某个列表中 便于输入保证元素的原子性
                    bill_no = row[0]
                    bill_state = row[1]
                    print "今天已交账未生成销售单的订单:", bill_no, '单据状态:', bill_state  # 打印检查结果
                    bill_info.append([bill_no, bill_state])  # 把结果存到列表 bill_info 中
                return bill_info
            else:
                # print  "    Congratulations! 今天一切正常, 全部生成销售单or退货单!"
                return "    Congratulations! 今天一切正常, 全部生成销售单or退货单!"
        except:
            print "Error:not fetch the date."
        cursor.close()  # 关闭sql游标
        mysql_con.commit()  # 提交sql执行结果
        mysql_con.close()  # 释放数据库连接

    @classmethod
    def send_email_html(cls, SMTP_host, from_account, from_password, to_account, subject, content):
        # 1.实例化SMTP
        global msg_b, msg_all
        smtp = smtplib.SMTP()
        # 2. 链接邮件服务器
        smtp.connect(SMTP_host)
        # 3. 配置发送邮箱的用户名和密码
        smtp.login(from_account, from_password)
        # 4. 配置发送内容msg
        if type(content) == str:  # 如果content传参为一个字符串则返回这个字符串 否则（列表）则把列表数据传到html表中
            msg = MIMEText(content, 'plain', 'utf-8')
        else:
            msg_head = """
                        <table color="CCCC33" width="500" border="1" cellspacing="0" cellpadding="10" text-align="center">
                            <tr>
                              <td text-align="center">未生成销售or退货单的订单号</td>
                              <td text-align="center">单据状态</td>
                            </tr>   """
            msg_body = ""
            for i in range(len(content)):  # 遍历二阶列表
                msg_b = ''' <tr>   
                             <td text-align="center"> %s </td>
                             <td text-align="center"> %s </td> 
                             </tr>
                            ''' % (content[i][0], content[i][1])
                # print content[i][0], content[i][1]
                msg_body += msg_b  # 累加各个数值
            msg_all = msg_head + msg_body + '''</table>'''  # 组合表头跟表体
            msg = MIMEText(msg_all, 'HTML', 'utf-8')  # 拼接邮件内容
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_account
        msg['To'] = ','.join(to_account)
        # 5. 配置发送邮箱，接收邮箱，以及发送内容
        smtp.sendmail(from_account, to_account, msg.as_string())
        # 6. 关闭邮件服务
        smtp.quit()

    @classmethod
    def send_email(cls, smtp_host, from_account, from_password, to_account, subject, content):
        # 1 实例化SMTP
        smtp = smtplib.SMTP()
        # 2 连接邮件服务器
        smtp.connect(smtp_host)
        # 3 录入发送邮箱的用户名密码
        smtp.login(from_account, from_password)
        # 4 加入邮件内容msg
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_account
        msg['To'] = ','.join(to_account)       #发送给多个邮件用户
        # 5 正式发送邮件
        smtp.sendmail(from_account, to_account, msg.as_string())


if __name__ == '__main__':
        start_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        end_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        sql = '''
            SELECT
    	    ssot.billNo AS '当天交账未生成销售单的单据',
            CASE MAX(ssot.billState)  
            WHEN 5 THEN '已签收'
            WHEN 4 THEN '待签收'
            WHEN 3 THEN '已入库/已出库'
            WHEN 2 THEN '待入库/待出库'
            WHEN 1 THEN '发送中'
            WHEN 0 THEN '已撤销'
            END AS '单据状态'
            FROM
    	      saas_erp_474.t_bill_sale_order_trade ssot
            WHERE
    	      concat(ssot.cid, '-', ssot.billNo) IN (
    		SELECT
    			fso.orderNo
    		FROM
    			00_fms.finance_business fso
    		WHERE
    			fso.accountTime BETWEEN '2017-10-19 00:00:00'
    		AND '2017-10-19 23:59:59'
    		AND fso.state = 3
    	   )
           GROUP BY
    	   ssot.billNo
           HAVING
    	   MAX(ssot.billState) NOT IN (6, 7);
            '''  # %(start_time, end_time)
        select_mysql = saleOrderCheck.connect_mysql_select('192.168.1.206', 'root', 'qazWSX098', 'saas_erp_409', sql)
        listMailSender=['taodongkan@163.com','864714820@qq.com']           #插入一个列表
        # for raw in select_mysql:
        #  print  raw
        send_mysql = saleOrderCheck.send_email_html('smtp.zhoupu123.com', 'taodongkan@zhoupu123.com', '1qaz!QAZ', listMailSender,
                                                                       '本邮件用于检测当天交账没生成的‘销售单or退货单’-by tdk', select_mysql)
