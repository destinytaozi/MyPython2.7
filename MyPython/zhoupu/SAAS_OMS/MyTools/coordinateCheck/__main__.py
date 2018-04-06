# coding=utf-8
# This file is used to check cloud sign Coordinate
from MyPython.zhoupu.BasicFunction.DBBasic.doVsMySQL import doVsMySQL

if __name__ == '__main__':
    dbUrl = "192.168.1.206"
    dbUsr = "root"
    dbPassword = "qazWSX098"
    dbBase = "ganyu_tms"
    sql = '''
          SELECT
           tds.omsCode,
	       tds.signNo,
           tds.signTime,
	       tds.consumerName,
	       tds.addrLat,
	       tds.addrLng,
	       tdco.addrLat,
	       tdco.addrLng
          FROM
	       ganyu_tms.t_distribution_sign tds
          LEFT JOIN ganyu_oss.t_doc_consumer_oss tdco ON tdco.id = tds.consumerId AND tdco.cid=tds.cid
          WHERE
	       tds.addrLat IS NOT NULL ORDER BY tds.consumerName
           '''
    doVsMySQL=doVsMySQL()
    con=doVsMySQL.connectMySQL(dbUrl,dbUsr,dbPassword,dbBase)
    cursor=doVsMySQL.getCursor(con)
    sqlResult=doVsMySQL.selectMySQL(cursor,sql)



