#coding=utf-8
'''
Created on 2016年11月30日

@author: Jane Wei
'''
#import xlrd
from libs.excel import excel
from libs.Locator import Locator
#from selenium import webdriver
from libs.logger import logger
from libs.MyException import MyException
from libs.base import Base

class pageObject(Base):
    '''
    classdocs
    '''
    logger = logger
    #def __init__(self, driver)
    def __init__(self):
        '''
        Constructor
        '''
        pass
        #self.driver = driver
        #self.pofile =  pageObjectFile
        #self.logger = logger
    
    '''def getLocatorMap(self,pagename):
        return excel(self.pofile,self.logger).getSheetMap(pagename)'''
    
    @classmethod 
    def getLocatorMap(cls,pageObjectFile,pageName):
        if pageObjectFile == '':
            raise MyException('Invalid page object file: "%s"'%pageObjectFile)        
        if pageName == '':
            raise MyException('Invalid sheet name: "%s"'%pageName)
        return excel(pageObjectFile).getSheetMap(pageName)
    
    @classmethod 
    #def getLocator(cls,pageObjectFile,pageName,locatorName):
    def getLocator(cls,pageObjectFile,*locator):
        if len(locator) ==1:
            pageName = 'Home'
        elif len(locator) == 2:
            pageName = locator[1]
            locatorID = locator[0]
        else:
            raise MyException('Invalid locator info: "%s"'%locatorID)
        
        if pageObjectFile == '':
            raise MyException('Invalid page object file: "%s"'%pageObjectFile) 
        
        cls.logger.debug(pageName)  
        cls.logger.debug(locatorID)  
        locatorMap = cls.getLocatorMap(pageObjectFile,pageName)
        #locator name    description    locate type    path
        for i in range(len(locatorMap)):
            if locatorMap[i][0] == locatorID:
                cls.logger.debug('locator ID: %s,locator Info: %s, type: %s'%(locatorMap[i][0],locatorMap[i][3],locatorMap[i][2]))
                return Locator(locatorMap[i][3],locatorMap[i][2],locatorMap[i][0],locatorMap[i][1])
        else:
            raise MyException('Not found locator "%s" definition in "%s"!'%(locatorID,pageObjectFile))
            #return Locator()
    
    