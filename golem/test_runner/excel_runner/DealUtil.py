import xlrd

class DealUtil:
    
    def __init__(self, path):
        self.data = xlrd.open_workbook(path)
    
    def getTableData(self, tableName):
        return self.data.sheet_by_name(tableName)

    def getRowValues(self, tableData, rowId):
        return tableData.row_values(rowId)

    @staticmethod
    def getAppInfo(path):
        dealUtils = DealUtil(path)
        tableData = dealUtils.getTableData('configure')
        titleRowValues = dealUtils.getRowValues(tableData, 0)
        appValues = dealUtils.getRowValues(tableData, 1)
        print("DealUtil=================")
        print(titleRowValues)
        print("titleRowValues2=================")
        print(appValues)

        return appValues[1], appValues[2], appValues[3]
        
    
if __name__ == "__main__":
    DealUtil.getAppInfo('C:/iTestin/framework/golem-master/projects/golem_e2e/testcaseExcel/login/keyword.xlsx')