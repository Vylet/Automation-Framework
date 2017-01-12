#coding=utf-8
'''
Created on 
'''
from appium.webdriver.common.mobileby import MobileBy as By

class Locator:
    def __init__(self,selector,byType='id',name="",desc=''):
        self.selector = selector
        #self.byType = byType
        self.name=name
        self.desc = desc
        self.setBy(byType)
        
    def getSelector(self):
        return self.selector
    
    def getType(self):
        #print self.byType 
        return self.byType  
    
    def setBy(self,byType):
        d = {'id':By.ID,
                'xpath': By.XPATH,
                'linkText': By.LINK_TEXT,
                'partialLinkText': By.LINK_TEXT,
                'name': By.NAME,
                'className': By.CLASS_NAME,
                'context-desc': By.ACCESSIBILITY_ID,
                'android': By.ANDROID_UIAUTOMATOR,
                'ios':By.IOS_UIAUTOMATION,
                'cssSelector': By.CSS_SELECTOR
                }
        self.byType=d.get(byType,By.ID)
        #print self.byType
    
    def getName(self):
        return self.name
