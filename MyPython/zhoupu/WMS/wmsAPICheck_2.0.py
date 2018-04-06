# coding=utf-8
# This is the file "wms_API_check.py"
# We use it to check the wms api
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import cx_Oracle


class wmsAPICheck:
    def __init__(self):
        pass

    def connectWMS(self,user_name, user_password, url_sid):
        try:
            conn = cx_Oracle.connect(user_name, user_password, url_sid)
            return conn
        except Exception,msg:
            return msg


    def getCursor(self,connect):
        cursor =connect.cursor()
        return cursor

    def selectSQL(self,cursor,sql):
        cursor.execute(sql)
        result = cursor.fetchall()
        count = cursor.rowcount
        print "Total:", count
        cursor.close()
        return result

    def closeConn(self,connect):
        connect.close()

    @classmethod
    def doVSResult(cls,user_name, user_password, url_sid, sql):
        wmsAPIchk=wmsAPICheck()
        getConn = wmsAPIchk.connectWMS(user_name, user_password, url_sid)
        getCurs = wmsAPIchk.getCursor(getConn)
        sqlResult = wmsAPIchk.selectSQL(getCurs,sql)
        rest_List=[]
        for row in sqlResult:
            bill_no = row[0]
            distributor = row[1]
            data_time = row[2]
            sheet_id = row[3]
            rest_List.append([bill_no, distributor,data_time,sheet_id])
        wmsAPIchk.closeConn(getConn)
        print  'Oracle connection has been closed!'
        return rest_List


    @classmethod
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

    def send_mail(cls, SMTP_host, from_account, from_password, to_account, subject, content):
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
                        <table color="CCCC33" width="500" border="1" cellspacing="0" cellpadding="10" align="center">
                            <tr>
                              <td align="center">未生成销售or退货单的订单号</td>
                              <td align="center">单据状态</td>
                            </tr>   """
            msg_body = ""
            for i in range(len(content)):  # 遍历二阶列表
                msg_b = ''' <tr>   
                             <td align="center"> %s </td>
                             <td align="center"> %s </td> 
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
        print 'Send mail successful！'
        # 6. 关闭邮件服务
        smtp.quit()

    @classmethod
    def montageStr(cls, api_confirm, api_description):
        global msg_body, msg_b
        if api_confirm:
            msg_head = '''
                        <tr>
                         <td align="center">序号</td>
                         <td align="center">%s</td>
                         <td align="center">cid</td>
                         <td align="center">sheetid</td>
                        </tr>
                            ''' % (api_description)
            msg_body = ""
            #if len(api_confirm)>30:
            #    length_api=30
            #    for i in range(length_api):
            #        msg_b = '''
            #                 <tr>
            #                 <td align="center">%s</td>
            #                 <td align="center">%s</td>
            #                 <td align="center">%s</td>
            #                 </tr>
            #                ''' % (i,api_confirm[i][0], api_confirm[i][1])
            #        msg_body += msg_b
            #    msg_all = msg_head + msg_body
            #else:
            for i in range(len(api_confirm)):
                msg_b = '''
                        <tr>
                             <td align="center">%s</td>
                             <td align="center">%s</td>
                             <td align="center">%s</td>
                             <td align="center">%s</td>
                        </tr>
                        ''' % (i+1,api_confirm[i][0], api_confirm[i][1],api_confirm[i][3])
                msg_body += msg_b
            msg_all = msg_head + msg_body
        else:
            msg_all = '''
                           <tr>
                             <td align="center" colspan = "4">%s</td>
                            </tr>
                       ''' % (api_description + "接口很干净，无数据残留！")
        return msg_all

    @classmethod
    def montageMsg(cls, outconf, reGoodsConf, inconf, factoryConf, lossConf,calcelR):
        msg_head = '''
                      <table color = "CCCC33" width = "500" border = "1" cellspacing = "0" cellpadding = "10" align = "left" >
                        <tr>
                          <td align ="center" colspan ="4"><strong>WMS接口排查（按时间先后顺序）</strong></td>
                        </tr>        
                  '''
        msg_tree = '''</table>'''
        msg_all = msg_head + outconf +calcelR+reGoodsConf + inconf + factoryConf  + lossConf   + msg_tree
        return msg_all

    def assembSQL(self,listCount,str):
        global assembNew,assemb
        assembNew=''
        assemb=''
        for i in range(len(listCount)):
            newCount = listCount[i][0]
            wmsNewCount="'"+newCount+"',"
            newCountall="'"+newCount[:-3]+"',"
            assembNew+=newCountall
            assemb+=wmsNewCount
        assembNewLeast=assembNew[:-1]
        if str =='出库':
            infirmSQL = '''
SELECT
	omsId,
	flowstate,
    CASE WHEN flowState in ('10010','10020','10030','10200') THEN
	'未出,不删除'
    ELSE
    '可以删除' END AS '标识'
FROM t_bill_sale_order WHERE omsId IN (%s);
            '''%(assembNewLeast)
            return infirmSQL + assemb[:-1]
        elif str == '进货':
            # infirmSQL = '''
            #                             SELECT
            # 	                             omsId,
            # 	                             flowstate,
            #                                  CASE WHEN flowState in ('10010','10020','10030','10200') THEN
            # 	                                 '未出,不删除'
            #                                  ELSE
            #                                      '可以删除' END AS '标识'
            #                             FROM t_bill_sale_order WHERE omsId IN (%s);
            #             ''' % (assembNewLeast)
            return '待完善'
        else:
            return '非常用接口，手动查询'




if __name__ == '__main__':
    wms_jk_account = 'zhpwms_jk'
    wms_jk_password = 'zhpwms_jk123'
    # wms_url = '116.62.34.14:1521/orcldb'
    wms_url = '114.215.253.158:1521/orcldb'
    SMTP_host_zp = 'smtp.zhoupu123.com'
    #SMTP_host_163 = 'smtp.163.com'
    from_account_zp = 'taodongkan@zhoupu123.com'
    #from_account_163 = 'taodongkan@163.com'
    from_password_zp = '1qaz!QAZ'
    #from_password_163 = ''
    listMailSender = ['864714820@qq.com','taodongkan@zhoupu123.com','shenhuanan@zhoupu123.com','wanghongxiang@zhoupu123.com']
    # listMailSender = ['864714820@qq.com','wanghongxiang@zhoupu123.com','taodongkan@zhoupu123.com','shenhuanan@zhoupu123.com','zhangxurong@zhoupu123.com','wuchunping@zhoupu123.com']
    subject = '现网WMS各回调接口巡检!'
    # 出库确认
    sql_outConfirm = '''
              select * from (select  distinct(wod.sourceexp_no),wod.owner_no ,wod.sdate,wod.sheetid from WTE_OM_DELIVER wod order by wod.sdate)
             '''
    # 入库确认
    sql_inConfirm = '''
              select * from (select  distinct(wic.po_no),wic.owner_no ,wic.sdate,wic.sheetid from WTE_IM_CHECK wic  order by wic.sdate) 
             '''

    # 退厂确认
    sql_factoryConfirm = '''
              select * from (select  distinct(wwd.po_no),wwd.owner_no ,wwd.sdate,wwd.sheetid from WTE_WM_DELIVER wwd  order by wwd.sdate) where rownum<=30
    '''

    # 退货确认
    sql_reGoodsConfirm = '''
              select * from (select  distinct(wuc.po_no),wuc.owner_no ,wuc.sdate,wuc.sheetid from WTE_UM_CHECK wuc  order by wuc.sdate) 
    '''

    # 报损确认
    sql_lossConfirm = '''
              select * from (select  distinct(wl.lost_no),wl.owner_no ,wl.sdate,wl.sheetid from WTE_LOST wl  order by wl.sdate) where rownum<=30
    '''

    # 库存调整
    sql_stockAdjust = '''
              select * from (select  distinct(wa.plan_no),wa.owner_no ,wa.sdate,wa.sheetid from WTE_ADJUST wa  order by wa.sdate) where rownum<=30
    '''

    # 出货订单取消回传
    sql_calcelRes = '''
            select * from (select  distinct(wocr.sourceexp_no),wocr.owner_no ,wocr.sdate,wocr.sheetid from WTE_OM_cancel_RESULT wocr order by wocr.sdate)
    '''

    outConfirm = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_outConfirm)
    inConfirm = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_inConfirm)
    factoryConfirm = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_factoryConfirm)
    reGoodsConfirm = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_reGoodsConfirm)
    lossConfirm = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_lossConfirm)
    # stockAdjust = wmsAPICheck.doVSResult(wms_jk_account, wms_jk_password, wms_url, sql_stockAdjust)
    calcelRes =wmsAPICheck.doVSResult(wms_jk_account,wms_jk_password,wms_url,sql_calcelRes)

    # wmschk=wmsAPICheck()
    # print wmschk.assembSQL(outConfirm,'出库')
    # print wmschk.assembSQL(inConfirm,'进货')
    # print wmschk.assembSQL(factoryConfirm,'退厂')
    # print wmschk.assembSQL(reGoodsConfirm,'退货')
    # print wmschk.assembSQL(lossConfirm,'报损')
    # print wmschk.assembSQL(stockAdjust,'库存')
    # print wmschk.assembSQL(calcelRes,'出库取消')

    # outConf = wms_API_check.montageStr(outConfirm, "出库确认")
    # reGoodsConf = wms_API_check.montageStr(reGoodsConfirm, "退货确认")
    # inConf = wms_API_check.montageStr(inConfirm, "入库确认")
    # factoryConf = wms_API_check.montageStr(factoryConfirm, "退厂确认")
    # lossConf = wms_API_check.montageStr(lossConfirm, "报损确认")
    # stockAdjust = wms_API_check.montageStr(stockAdjust, "调账确认")

    outConf = wmsAPICheck.montageStr(outConfirm, "出库确认(WTE_OM_DELIVER)")
    inConf = wmsAPICheck.montageStr(inConfirm, "入库确认(WTE_IM_CHECK)")
    factoryConf = wmsAPICheck.montageStr(factoryConfirm, "退厂确认(WTE_WM_DELIVER)")
    reGoodsConf = wmsAPICheck.montageStr(reGoodsConfirm, "退货确认(WTE_UM_CHECK)")
    lossConf = wmsAPICheck.montageStr(lossConfirm, "报损确认(WTE_LOST)")
    # stockAdj = wmsAPICheck.montageStr(stockAdjust, "调账确认(WTE_ADJUST)")
    calcelR = wmsAPICheck.montageStr(calcelRes,"出库取消(WTE_OM_CANCEL_RESULT)")

    content = wmsAPICheck.montageMsg(outConf, reGoodsConf, inConf, factoryConf, lossConf,calcelR)
    wmsAPICheck.send_mail_2array(SMTP_host_zp, from_account_zp, from_password_zp, listMailSender, subject, content)
