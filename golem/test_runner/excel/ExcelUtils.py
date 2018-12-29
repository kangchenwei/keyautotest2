# import xlrd
import xlrd
import time

class ExcelUtils:

    def __init__(self, filePath,driver):
        self.data = xlrd.open_workbook(filePath)
        self.driver = driver

    def getTableData(self,tableName):
        return self.data.sheet_by_name(tableName)

    def getRowValues(self,tableData,rowId):
        return tableData.row_values(rowId)


    #默认执行第一个sheet
    def execute(self):
        print('hello')

    #执行路径为filePath,sheet名字是sheetName的Excel
    @staticmethod
    def execute(filePath, sheetName, driver):

        excelUtils = ExcelUtils(filePath, driver)
        tableData = excelUtils.getTableData(sheetName)
        print("tabledata=========================")
        print(tableData)
        titleRowValues = excelUtils.getRowValues(tableData, 0)
        print("titleRowValues=========================")
        print(titleRowValues)

        ##这里仅仅是做了执行，如果要转换成py脚本，跟这个思路类似，略有不同

        print(tableData.col_values(0))
        for i in range(len(tableData.col_values(0))):
            if i == 0:
                continue
            rowValues = excelUtils.getRowValues(tableData, i)
            print("------------------------------------------")
            print(rowValues)

            keyDescription = ''
            keyAction = ''
            keyFindWay = ''
            keyElement = ''
            keyValue = ''
            for j in range(len(rowValues)):
                key = titleRowValues[j]
                if key == 'Model':
                    print('model')
                elif key == 'step description':
                    keyDescription = rowValues[j]
                    print(keyDescription)
                elif key == 'Action':
                    keyAction = rowValues[j]
                    print(keyAction)
                elif key == 'FindWay':
                    keyFindWay = rowValues[j]
                    print(keyFindWay)
                elif key == 'Element':
                    keyElement = rowValues[j]
                    print(keyElement)
                elif key == 'Value':
                    keyValue = rowValues[j]
                    print(keyValue)
                else:
                    print('is not valid key:'+rowValues[j])
            #判断关键字的类型，分别对应进行操作
            # if keyAction == 'sleep':
            #     time.sleep(keyValue)
            # if keyFindWay == '' or keyElement == '':
            #     #为了节省时间，这里只考虑到常规的查找控件然后操作，对于坐标类的，启动app类的都没做考虑
            #     continue
            # element = excelUtils.getElement(keyFindWay, keyElement)
            # print("element------------")
            # print(element)
            # if keyAction == '' or element == '':
            #     continue

            excelUtils.doOperation(excelUtils, keyAction, keyFindWay, keyElement, keyValue)

    #根据信息获取相应的元素
    def getElement(self, findWay, value):
        if findWay == 'find_element_by_xpath':
            return self.driver.find_element_by_xpath(value)
        elif findWay == 'find_element_by_id':
            return self.driver.find_element_by_id(value)
        elif findWay == 'find_element_by_class':
            return self.driver.find_element_by_class(value)
        elif findWay == 'find_element_by_name':
            return self.driver.find_element_by_name(value)
        return ''
        #以此类推，往下写

    # 根据控件类型执行相应的操作
    def doOperation(self, excelUtils, keyaction, keyfindway, keyelement, keyvalue):
        if keyaction == 'sleep':
            time.sleep(keyvalue)
        elif keyaction == 'click':
            element = excelUtils.getElement(keyfindway, keyelement)
            element.click()
        elif keyaction == 'send_keys':
            element = excelUtils.getElement(keyfindway, keyelement)
            element.send_keys(keyvalue)
        elif keyaction == 'set_text':
            element = excelUtils.getElement(keyfindway, keyelement)
            element.set_text(keyvalue)
        elif keyaction == 'swipe':
            coordinates = keyvalue.split(',')
            self.driver.swipe(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
        elif keyaction == 'close_app':
            self.driver.close_app()
        elif keyaction == 'remove_app':
            self.driver.remove_app(keyvalue)
        elif keyaction == 'implicitly_wait':
            self.driver.implicitly_wait(keyvalue)
        # 以此类推往下写