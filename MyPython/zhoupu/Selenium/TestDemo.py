# coding=GBK
# This file named switchSAASLogin.py
# His duty is switch distributor number in sysadmin and operAdmin.

from selenium import webdriver
import time
from selenium.webdriver import ActionChains


class Demo():
    def __init__(self):
        pass

    def openUrl(self,url):
        driver.get(url)
        headElement = driver.find_element_by_xpath("//*[@id='u1']/a[9]")
        ActionChains(driver).move_to_element(headElement).perform()


if __name__ == '__main__':
    myUrl = "https://www.baidu.com"
    driver = webdriver.Chrome()
    demoTest = Demo()
    demoTest.openUrl(myUrl)

