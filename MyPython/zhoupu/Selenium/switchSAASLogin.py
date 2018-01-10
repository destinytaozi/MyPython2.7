# coding=utf-8
# This file named switchSAASLogin.py
# His duty is switch distributor number in sysadmin and operAdmin.

from selenium import webdriver
import time
from selenium.webdriver import ActionChains


class switchSAASLogin():

    def __init__(self):
        pass

    def login_saas(self,url, userName, password):
        driver.maximize_window()
        driver.get(url)
        driver.find_element_by_id("remberme").click()
        driver.find_element_by_id("userName").send_keys(userName)
        driver.find_element_by_id("pwd").send_keys(password)
        driver.find_element_by_id("login_id").click()
        time.sleep(1)

    def getDestributor(self,distributor):
        salesMan = []
        if distributor == '519' or '欣丰多' in distributor:
            salesMan.append('13305128088')
            return salesMan
        elif distributor == '164' or '长青' in distributor:
            salesMan.append('13851208579')
            return salesMan
        elif distributor == '220' or '万揽' in distributor:
            salesMan.append('18344856789')
            return salesMan
        elif distributor == '454' or '申易通' in distributor:
            salesMan.append('15061373108')
            return salesMan
        elif distributor == '510' or '中心百货' in distributor:
            salesMan.append('13905126290')
            return salesMan
        elif distributor == '721' or '群琅' in distributor:
            salesMan.append('18168121788')
            return salesMan
        elif distributor == '844' or '赣榆邮政' in distributor:
            salesMan.append('13805128251')
            return salesMan
        elif distributor == '835' or '邮掌柜' in distributor:
            salesMan.append('15371668777')
            return salesMan
        elif distributor == '127' or '富祥' in distributor:
            salesMan.append('15961319566')
            return salesMan
        elif distributor == '743' or '君畅' in distributor:
            salesMan.append('15371668288')
            return salesMan
        elif distributor == '656' or '统仓统配生产验证' in distributor:
            salesMan.append('18950005001')
            return salesMan
        else:
            return '非云仓用户,联系管理员添加账号'

    def openSettingMenu(self,distributionGet):
        saleElementPath = driver.find_element_by_xpath("//*[@id='mainMenu']/div[2]/div[1]/b")
        ActionChains(driver).move_to_element(saleElementPath).perform()                    #定位鼠标到一级菜单“设置”
        mouseClickjs = '''
                          var evObj = document.createEvent('MouseEvents');
                          evObj.initMouseEvent("click",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                          arguments[0].dispatchEvent(evObj);
                      '''
        sysSetUserMenuPath = driver.find_element_by_xpath("/html/body/div[11]/div[5]/div")
        driver.execute_script(mouseClickjs, sysSetUserMenuPath)  # 定位鼠标到二级菜单“用户”并点击
        driver.switch_to.frame("system/user/list")
        time.sleep(1)
        oprAmountPath = driver.find_element_by_xpath(".//div[contains(@class,'datagrid-view')]/div[2]/div[2]/table/tbody/tr[4]/td[contains(@field,'opt')]/div/span/a[contains(@title,'修改关联用户')]")#修改关联用户
        time.sleep(1)
        driver.execute_script(mouseClickjs, oprAmountPath)      #定位鼠标到修改关联用户编辑按钮处并点击
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='fm']/div/table/tbody/tr[3]/td/div/span/input[1]").send_keys(distributionGet[0]) #把经销商电话填入弹出框
        time.sleep(1)
        # userListPath = driver.find_element_by_xpath(".//div[contains(@class,'panel combo-p') and contains(@style,'position: absolute')]/div[contains(@class,'panel-body-noheader')]/div[1]")#有问题 待优化
        userListPath = driver.find_element_by_xpath(".//body[contains(@class,'easyui-layout iframe-body-common')]/div[contains(@class,'panel combo-p')]/div[contains(@class,'combo-panel panel-body')]/div[1]")
        driver.execute_script(mouseClickjs,userListPath) #选中
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/a[1]/span/span").click() #点保存
        time.sleep(1)

    def set_consumerInfo(self,consumerName,salesMan,wareHouse,bakInfo):
        driver.find_element_by_xpath("//*[@id='billForm']/div[1]/div[2]/ul/li[1]/span/input[1]").send_keys(consumerName)



    def set_goodsInfo(self,goodsName,saleQuantity,saleCount,bakInfo):
        return 0

    def set_submitSaleOrder(self):
        return 0

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
                                 "统仓统配生产验证:656\n"
                                 "请输入要登录的cid或者经销商名: ")

    pwd = "aA111111"
    driver = webdriver.Chrome()
    saasAuto = switchSAASLogin()
    distributionGet = saasAuto.getDestributor(distributorInput)
    print distributionGet
    # saasAuto.login_saas(sysUrl, sysUserName, sysPassword)
    # saasAuto.openSettingMenu(distributionGet)
    # driver.close()
    # driver = webdriver.Chrome()
    saasAuto.login_saas(sysUrl,oprUserName,oprPassword)





