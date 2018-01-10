# coding=utf-8

from MyPython.zhoupu.BasicFunction.DBBasic.doVsMySQL import doVsMySQL
from MyPython.zhoupu.SAAS_OMS.MyTools.prdSaasSwitch.switchSAASLogin import switchSAASLogin
from selenium import webdriver

if __name__ == '__main__':
    sysUrl = "https://www.zhoupu123.com/saas/tologin"
    # sysUrl = "http://192.168.1.212/saas/tologin"
    sysUserName = "sysadmin"
    sysPassword = "RC33fWugPaAQQ3xBSumEDhuNP4fvyHoZ"
    oprUserName = "operadmin"
    oprPassword = "NxMVaaFJl63rZTYBuX8mxNeDxdPojqAi"
    distributorInput = raw_input("欣丰多:519\n"
                                 "长青:164\n"
                                 "万揽:220\n"
                                 "申易通:454\n"
                                 "中心百货:510\n"
                                 "群琅:721\n"
                                 "赣榆邮政:844\n"
                                 "邮掌柜:835\n"
                                 "富祥:127\n"
                                 "君昌:743\n"
                                 "请输入要登录的cid: ")

    pwd = "aA111111"

    dbUrl_pre = "114.55.2.138"
    dbUsr = "root"
    dbPW = "qazWSX098"
    dbBase = "saas_common_prd_0612"
    driver = webdriver.Chrome()
    saasAuto = switchSAASLogin()
    dbSQL = saasAuto.getDestributorSQL(distributorInput) #获取cid后在common库sysorg表去查询手机号
    # print dbSQL
    doVsMySQL = doVsMySQL()
    conMysql = doVsMySQL.connectMySQL(dbUrl_pre,dbUsr,dbPW,dbBase)
    getCursor = doVsMySQL.getCursor(conMysql)
    selectSQL = doVsMySQL.selectMySQL(getCursor,dbSQL)
    distributionGet = selectSQL[0]
    saasAuto.login_saas(driver,sysUrl, sysUserName, sysPassword)
    saasAuto.openSettingMenu(driver,distributionGet)
    driver.close()
    driver = webdriver.Chrome()
    saasAuto.login_saas(driver,sysUrl,oprUserName,oprPassword)