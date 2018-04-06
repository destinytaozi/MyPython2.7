# coding=utf-8
from selenium import webdriver
import time

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# browser = webdriver.Chrome(chrome_options=options)
# browser.get("http://www.baidu.com/")
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
from selenium.webdriver import ActionChains


class autoNewSaleOrder():
    global mouseClickjs
    mouseClickjs = '''
                      var evObj = document.createEvent('MouseEvents'); 
                      evObj.initMouseEvent("click",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                      arguments[0].dispatchEvent(evObj);
                   '''

    def __init__(self):
        pass

    def login_oms_saas(self,url, userName, password):
        driver.get(url)
        print driver.title
        driver.find_element_by_id("remberme").click()
        driver.find_element_by_id("userName").send_keys(userName)
        driver.find_element_by_id("pwd").send_keys(password)
        driver.find_element_by_id("login_id").click()
        time.sleep(3)

    def enter_sale_Order(self,):
        saleElement = driver.find_element_by_xpath("//*[@id='mainMenu']/div[2]/div[1]")
        ActionChains(driver).move_to_element(saleElement).perform()                    #定位鼠标到一级菜单“销售”
        # mouseOverjs = '''
        #                  var evObj = document.createEvent('MouseEvents');
        #                  evObj.initMouseEvent("mouseover",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        #                  arguments[0].dispatchEvent(evObj);
        #                  '''
        mouseClickjs = '''
                          var evObj = document.createEvent('MouseEvents'); 
                          evObj.initMouseEvent("click",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                          arguments[0].dispatchEvent(evObj);
                      '''
        saleOrderPath = driver.find_element_by_xpath("/html/body/div[11]/div[4]/div")
        # driver.execute_script(mouseOverjs,saleOrderElement)
        driver.execute_script(mouseClickjs, saleOrderPath)     #定位鼠标到二级菜单“销售订单”并点击

    def set_consumerInfo(self,consumerName,salesMan,wareHouse,bakInfo):
        driver.find_element_by_xpath("//*[@id='billForm']/div[1]/div[2]/ul/li[1]/span/input[1]").send_keys(consumerName)
        saleOrderPat





    def set_goodsInfo(self,goodsName,saleQuantity,saleCount,bakInfo):
        return 0

    def set_submitSaleOrder(self):
        return 0



if __name__ == '__main__':
    saasUrl = "http://192.168.1.212/saas/tologin.html"
    omsUrl = "https://cloud.zhoupu123.com/oss/main"
    saasUName_pre = "https://erp.zhoupu123.com/saas/tologin"
    saasUName_0801 = "15061373108"  # 申易通 cid:454 db: saas_erp_409
    saasUName_newMaser = "13305128089"  # 欣丰多 cid:519 db:saas_erp_474
    omsUserName = "sysadmin"
    pwd = "aA111111"
    driver = webdriver.Chrome()
    omsAuto = autoNewSaleOrder()
    omsAuto.login_oms_saas(saasUrl, saasUName_0801, pwd)
    omsAuto.new_saleOrder()
