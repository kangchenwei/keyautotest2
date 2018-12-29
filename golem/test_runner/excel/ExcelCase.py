#coding:utf-8
from appium import webdriver
import time
import unittest
import os
# from golem.test_runner.BeautifulReport.BeautifulReport import BeautifulReport
from selenium.webdriver.support.ui import WebDriverWait

from golem.test_runner.excel.ExcelUtils import ExcelUtils


class ExcelCase(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android' #Android系统 or IOS系统
        desired_caps['deviceName'] = 'KVD6JZ7999999999' #真机或模块器名
        desired_caps['platformVersion'] = '5.0.2' #Android系统版本
        desired_caps['appPackage'] = 'com.kuaikan.comic'  #APP包名
        desired_caps['appActivity'] = 'com.kuaikan.comic.ui.LaunchActivity' #APP启动Activity
        # desired_caps['noReset']=True #每次打开APP不开启重置，否则每次都进入四个欢迎页
        # desired_caps['resetKeyboard'] = True #隐藏键盘
        # desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['app'] = 'C:/康宸维的小空间/研究生/关键字脚本解析/origin.apk'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps) #启动APP

    def test_executeExcel(self):
        excelPath = 'C:/iTestin/framework/golem-master/testcaseExcel/keyword.xlsx'
        tableName = 'test'
        ExcelUtils.execute(excelPath, tableName, self.driver)

    def tearDown(self):
        print('teardown')
        self.driver.quit()


if __name__ == '__main__':
    #构造测试套件
    suite = unittest.TestSuite()
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&")
    suite.addTest(ExcelCase("test_executeExcel"))
    #按照一定格式获取当前时间
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    print("*************************************88")
    print(now)
    ##将当前时间加入到报告文件名称中，定义测试报告存放路径
    filename='/Users/jinweiguang/jwg/TESTIN/test/result.html'


    # result = BeautifulReport(suite)
    # result.report(filename='测试报告', description='测试deafult报告', log_path='.')

    # #定义测试报告
    # fp=open(filename,'wb')
    # runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试报告',description='用例执行情况:')
    # runner.run(suite)
    # #关闭报告
    # fp.close()
