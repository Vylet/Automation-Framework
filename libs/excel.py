#coding=utf-8
'''
Created on 2016年11月30日

@author: Jane Wei
'''
import xlrd
from libs import logger

class excel(object):
    '''
    common class to handle excel file
    '''
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.file = filename
        self.logger = logger.logger
        
    def getSheetMap(self,sheetname): 
        with xlrd.open_workbook(self.file) as f:
            table = f.sheet_by_name(sheetname)
            nrows = table.nrows
            ncols = table.ncols
            list1 = []
            
            for i in range(1,nrows):
                tmp = []
                for j in range(ncols):
                    try:
                        #ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                        #http://www.68idc.cn/help/jiabenmake/python/20150301238491.html
                        if (type(table.cell(i,j).value)==float) and (table.cell(i,j).value == int(table.cell(i,j).value)):
                                val = int(table.cell(i,j).value)
                                #print val
                                #print type(val)
                                tmp.append(unicode(val))
                        else:
                            tmp.append(table.cell(i,j).value)
                    except Exception,e:
                        self.logger.error(e)
                list1.append(tmp)
            return list1  