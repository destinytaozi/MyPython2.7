# coding=utf-8
# This file named switchSAASLogin.py
# His duty is switch distributor number in sysadmin and operAdmin.
import time

from MyPython.zhoupu.BasicFunction.DBBasic.doVsMySQL import doVsMySQL
from selenium import webdriver
from selenium.webdriver import ActionChains


class switchSAASLogin():
    def __init__(self):
        pass

    #登录saas
    def login_saas(self,driver,url, userName, password):
        driver.maximize_window()
        driver.get(url)
        driver.find_element_by_id("remberme").click()
        driver.find_element_by_id("userName").send_keys(userName)
        driver.find_element_by_id("pwd").send_keys(password)
        driver.find_element_by_id("login_id").click()
        time.sleep(3)

    #用cid查询经销商手机号
    def getDestributorSQL(self,distributor):
        sql = '''SELECT tsu.phone phone,tso.`name` name,tso.id cid 
                            FROM t_sysorg tso 
                            INNER JOIN t_sysuser tsu 
                            ON tso.id=tsu.sysorgid 
                            WHERE tsu.uid=1 AND tso.id=%s'''%(distributor)
        return sql


    #页面元素操作
    def openSettingMenu(self,driver,distributionGet):
        # protocolElementPath=
        driver.find_element_by_xpath("/html/body/div[16]/div/a").click() #关闭协议
        ActionChains(driver)
        saleElementPath = driver.find_element_by_xpath("//*[@id='mainMenu']/div[2]/div[1]/b")
        ActionChains(driver).move_to_element(saleElementPath).perform()                    #定位鼠标到一级菜单“设置”
        mouseClickjs = '''
                          var evObj = document.createEvent('MouseEvents');
                          evObj.initMouseEvent("click",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                          arguments[0].dispatchEvent(evObj);
                      '''
        sysSetUserMenuPath = driver.find_element_by_xpath("/html/body/div[contains(@class,'file-und-menu menu')]/div[contains(@url,'system/user/list')]/div[contains(@class,'menu-text')]")
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

    def set_consumerInfo(self,driver,consumerName,salesMan,wareHouse,bakInfo):
        driver.find_element_by_xpath("//*[@id='billForm']/div[1]/div[2]/ul/li[1]/span/input[1]").send_keys(consumerName)



    def set_goodsInfo(self,goodsName,saleQuantity,saleCount,bakInfo):
        return 0

    def set_submitSaleOrder(self):
        return 0







