# -*- coding:utf-8 -*-
import cx_Oracle



if __name__ == '__main__':
    conn = cx_Oracle.connect('zhpwms_jk', 'zhpwms_jk123', '116.62.34.14:1521/orcldb')
    #dsn_tns = cx_Oracle.makedsn('192.168.1.143', 1521, 'orcldb') #测试连接成功
    #print dsn_tns
    cursor = conn.cursor()
    sql='''
        select t.po_no as billno  
        ,case t.owner_no 
        when '00510' then '赣榆中心百货' 
        else '其他' end as distributor 
        from WTE_UM_CHECK t'''

    cursor.execute(sql)
    results= cursor.fetchall()
    count = cursor.rowcount
    print "Total:",count
    restList = []
    for row in results:
        billno=row[0]
        distributor=row[1]
        restList.append([billno,distributor])

