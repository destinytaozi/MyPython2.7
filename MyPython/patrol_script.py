# -*- coding: utf-8 -*-
# This is the file "patrol_script.py"
# We use it to check the accounted sale order bill is function normal.
import datetime

import saleOrderCheck

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
        '''#%(start_time, end_time)
    select_mysql = saleOrderCheck.saleOrderCheck.connect_mysql_select('192.168.1.206', 'root', 'qazWSX098', 'saas_erp_409', sql)
    #for raw in select_mysql:
     #  print  raw
    send_mysql = saleOrderCheck.saleOrderCheck.send_email_withhtml('smtp.163.com', 'taodongkan@163.com', '8uhb*IK<',
                                          '864714820@qq.com', '本邮件用于检测当天交账没生成的‘销售单or退货单’-by tdk', select_mysql)