import MySQLdb


def getInitialValue(url, name, password, dbName, sql):
    mysql_con = MySQLdb.connect(url, name, password, dbName)
    cursor = mysql_con.cursor()