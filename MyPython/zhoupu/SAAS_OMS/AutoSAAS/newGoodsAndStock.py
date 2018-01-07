# -*- coding: utf-8 -*-
# This is the file "newGoodsAndStock.py"
# We use it to new goods and give the stock
import MySQLdb

class myGoods():
    def con_Mysql(self, url, user, password, db_name, sql):
        result_list = []
        conn = MySQLdb.connect(url, user, password, db_name,charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result_list.append(row)
            print  row
        return result_list

    def newGoods(self):
        return 0


if __name__ == '__main__':
    db_url = '192.168.1.206'
    db_user = 'root'
    db_password = 'qazWSX098'
    db_base = 'saas_erp_409'
    my_sql = '''select * from t_doc_goods
             '''
    query_result = []
    query_result = myGoods.con_Mysql('192.168.1.206', 'root', 'qazWSX098', 'saas_erp_409', my_sql)
    for i in range(len(query_result)):
        print  query_result[i]
