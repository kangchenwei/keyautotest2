#coding:utf-8
import sys

from appium import webdriver
import time
import unittest
import HTMLTestRunner
from BeautifulReport import BeautifulReport
import os
# from golem.test_runner.BeautifulReport.BeautifulReport import BeautifulReport
from selenium.webdriver.support.ui import WebDriverWait

from golem.test_runner.excel_runner.DealUtil import DealUtil
from golem.test_runner.excel_runner.ExcelUtils import ExcelUtils
from golem.test_runner.excel_runner.ParametrizedTestCase import ParametrizedTestCase


class ExcelCase(unittest.TestCase):

    def __init__(self, test_name, cases_path, project_name):
        super(ExcelCase, self).__init__(test_name)
        self.test_name = test_name
        self.cases_path = cases_path
        self.project_name = project_name

    def setUp(self):
        app, appPackage, appActivity = DealUtil.getAppInfo(self.cases_path)
        self.desired_caps = {}
        self.desired_caps['app'] = app
        self.desired_caps['appPackage'] = appPackage  # APP包名
        self.desired_caps['appActivity'] = appActivity  # APP启动Activity
        self.desired_caps['platformName'] = 'Android' #Android系统 or IOS系统
        self.desired_caps['deviceName'] = 'KVD6JZ7999999999' #真机或模块器名
        self.desired_caps['platformVersion'] = '5.0.2' #Android系统版本
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps) #启动APP

    def test_executeExcel(self):
        excelPath = self.cases_path
        # excelPath = 'C:/iTestin/framework/golem-master/testcaseExcel/keyword.xlsx'
        tableName = 'testcase'
        ExcelUtils.execute(excelPath, tableName, self.driver)

    def tearDown(self):
        print('teardown')
        self.driver.quit()


# 用例目录
test_suite_dir = r'C:\Users\Administrator\PycharmProjects\OpenAPI_new\\'
# test_suite_dir=r'/opt/openapi/'  #145部署环境
# 报告目录
Report_dir = r'C:\Users\Administrator\PycharmProjects\OpenAPI_new\Report\\'
# Report_dir=r'/opt/openapi/Report/'  #145部署环境

def creatsuite():
    testunit = unittest.TestSuite()
    # 定义测试文件查找的目录
    test_dir = test_suite_dir
    # 定义 discover 方法的参数
    package_tests = unittest.defaultTestLoader.discover(test_dir,
                                                        pattern='Test*.py',
                                                        top_level_dir=None)
    # package_tests=TestLoader.discover(start_dir=test_dir, pattern='Test*.py')
    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in package_tests:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print(testunit)
    return testunit


alltestnames = creatsuite()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(argv)
    
    #要动态传入项目名、测试套件还是测试用例、测试套件文件、测试用例目录
    base_path = "C:/iTestin/framework/golem-master/projects/"
    if argv[2] == 'testcases': #判断测试类别是suites还是testcases,从而确定目录
        test_category = 'testcaseExcel'
    elif argv[2] == 'suites':
        test_category = 'suites'

    print("----111111111111---")
    print(test_category)
        
    cases_path = base_path + argv[1] + '/' + test_category + '/' + argv[3]

    print("---------2222222222222--------")
    print(cases_path)
    # 构造测试套件
    suite = unittest.TestSuite()
    suite.addTest(ExcelCase("test_executeExcel", cases_path, argv[1]))
    # suite.addTest(ExcelCase("test_executeExcel"))
    # 按照一定格式获取当前时间
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    ##将当前时间加入到报告文件名称中，定义测试报告存放路径
    test_report = 'C:/iTestin/framework/golem-master/testcaseExcel/report/result.html'

    # discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    result = BeautifulReport(suite)
    result.report(filename='测试报告2', description='测试deafult报告', log_path='./../../../testcaseExcel/report')

    # #定义测试报告
    # fp = open(test_report, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况:', verbosity=2)
    # runner.run(suite)
    # #关闭报告
    # fp.close()

if __name__ == "__main__":
    # sys.exit(main())
    # 启动appium服务  os.system('start startAppiumServer.bat')
    #传入参数：项目名称、suites还是testcases、要测试的目录或者文件
    main(sys.argv)
    # 关闭appium服务 os.system('start stopAppiumServer.bat')