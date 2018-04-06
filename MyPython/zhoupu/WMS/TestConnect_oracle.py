import cx_Oracle
def hello():
    conn = cx_Oracle.connect("zhpwms_jk/zhpwms_jk123@114.215.253.158/orcldb")
    cur = conn.cursor()
    try:
        print "Oralce Version:%s"%conn.version
        print "Table ETW_CUST is:"
        cur.execute("select * from ETW_CUST t where rownum<10")
        for row in cur:
            print row
    finally:
        cur.close()
        conn.close()

