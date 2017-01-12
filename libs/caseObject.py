#coding: utf-8
'''
Created on 2016年11月30日

@author: Jane Wei
'''
import unittest
from proboscis.asserts import assert_equal
from libs.excel import excel
from libs.pageObject import pageObject
from libs.logger import logger
from libs.base import Base
from libs.MyException import verificationErrors
import re

class caseObject(Base):
    
    def __init__(self,caseFile,pageObjectFile):
        self.caseFile = caseFile
        self.pofile = pageObjectFile
        self.logger = logger
        self.verificationErrors=verificationErrors

    def __del__(self):
        self.driver.quit()
        self.verificationErrors = []
        #assert_equal([], self.verificationErrors)
    
    def testCase(self,caseName,stepPrefix=0):        
        caseName=caseName 
        caseSteps = self.getSteps(caseName)
        i=0
        
        self.logger.debug('Number of lines: %d'%len(caseSteps))
        while i < len(caseSteps):
            item = caseSteps[i]
            if stepPrefix:
                self.logger.info('Line %s.%d: %s'%(stepPrefix,i+1,item[1]))
            else:
                self.logger.info('Line %d: %s'%(i+1,item[1]))
            #operation    description    locator1    locator2  para1 param2
            operator = item[0]
            if operator == '':
                i=i+1
                continue       
            
            #operation    description    locator1    locator2  para1(arg1,list) param2(arg2,dict)  
            #用法 driver.tap([(x,y),(x1,y1)],500)         
            #swipe(self, start_x, start_y, end_x, end_y, duration=None) 
            #driver.swipe(x1,y1,x2,y2,500) 
            #flick(self, start_x, start_y, end_x, end_y)
            #hide_keyboard(self, key_name=None, key=None, strategy=None) 
            #keyevent(self, keycode, metastate=None) 
            #press_keycode(self, keycode, metastate=None)
            #long_press_keycode(self, keycode, metastate=None)
            elif operator in ['openApp','tap','swipe','flick','hide_keyboard','keyevent','press_keycode','long_press_keycode']:
                try:
                    #arg1 = item[4].split(',')
                    self.logger.debug(item[4])
                    arg1 = item[4]
                    if item[4]:
                        arg1 = eval(item[4])
                    
                    self.logger.debug(2)
                    #arg2 is useless for tap and others
                    arg2 = self.str2Dict(item[5])
                    
                    self.logger.debug(3)
                    self.getOperation(operator,*arg1,**arg2)
                except Exception,e:
                    self.handleExcept(i, operator, e)  
            
            elif operator in ['click','clear']:
                try:
                    loc1 = item[2].split(':')
                    locator = pageObject.getLocator(self.pofile, *loc1)
                    self.getOperation(operator,locator)
                except Exception,e:
                    self.handleExcept(i, operator, e)      
                
            #scroll(self, origin_el, destination_el)
            #drag_and_drop(self, origin_el, destination_el):   
            elif operator in ['drag_and_drop','scroll']:
                try:
                    loc1 = item[2].split(':')
                    loc2 = item[3].split(':')
                    
                    slocator = pageObject.getLocator(self.pofile, *loc1)
                    dlocator = pageObject.getLocator(self.pofile, *loc2)
                    self.getOperation(operator,slocator,dlocator)
                except Exception,e:
                    self.handleExcept(i, operator, e)  
                
            #pinch(self, element=None, percent=200, steps=50)  
            # zoom(self, element=None, percent=200, steps=50)
            elif operator in ['pinch','zoom']:
                try:
                    loc1 = item[2].split(':')
                    arg1 = item[4].split(',')

                    locator = pageObject.getLocator(self.pofile, *loc1)
                    self.getOperation(operator,locator,*arg1)
                except Exception,e:
                    self.handleExcept(i, operator, e)   

            elif operator in ['reset','shake','open_notifications']:
                try:
                    self.getOperation(operator)
                except Exception,e:
                    self.handleExcept(i, operator, e) 
                        
            elif re.match('if|else if', operator):
                try:
                    op = operator.split(':')
                    
                    #verify condition
                    #operation    description    locator1    locator2 para1 param2 para3
                    loc1 = item[2].split(':')
                    attr = item[3] #condition
                    exp =  item[4]
                        
                    locator = pageObject.getLocator(self.pofile, *loc1)
                    #result = self.verify('verify_true',locator,attr)
                    #self.logger.debug('verify element "%s" "%s"'%(loc1[0],attr))
                    result = self.verify(op[1],locator,attr)
                    self.logger.debug(result)
                    if result:
                        self.logger.debug('Execute cases in sheet "%s"'%item[5])
                        trueCase = item[5]
                        self.testCase(trueCase,i+1)
                        self.logger.debug(item[6])
                        if item[6]:
                            self.logger.debug('assign new line number to i')
                            i = i+int(item[6])
                            continue
                        #self.logger.debug("Next step is %d"%(i+1))

  
                except Exception,e:
                    self.handleExcept(i, operator, e) 
                        
            elif operator in ['else']:
                try:
                    case =item[5]
                    self.testCase(case,i+1)
                except Exception,e:
                    self.handleExcept(i, operator, e) 
                        
            elif re.match('verify', operator):
                self.logger.debug('entering verify...')
                try:
                    loc1 = item[2].split(':')
                    attr = item[3] #condition
                    exp =  item[4]
                    self.logger.debug(loc1)
                    locator = pageObject.getLocator(self.pofile, *loc1)
                    result = self.verify(operator,locator,attr,exp)
                    self.logger.debug(result)
                    if result:
                        self.handlePass(i, operator)
                        #self.logger.info("STEP: %d %s ==>PASS "%(i+1,operator))
                    else:
                        self.handleFail(i, operator)
                        #self.logger.info("STEP: %d %s ==>FAIL "%(i+1,operator))
                        #self.verificationErrors.append("STEP: %d %s ==>FAIL "%(i+1,operator))
                except Exception,e:
                    self.handleExcept(i, operator, e) 
                
            i=i+1 
                    
        assert_equal([], self.verificationErrors)
     
    def getSteps(self,caseName):
        return excel(self.caseFile).getSheetMap(caseName)
    
    def handleExcept(self,step,op,err):
        self.verificationErrors.append('Line %s=> %s: %s'%(step+1,op,str(err) ))
        self.logger.error('Line %s=> %s: %s'%(step+1,op,str(err) )) 
    
    def handlePass(self,step,operator):
        self.logger.info("RESULT: %d %s ====>PASS "%(step+1,operator))
    
    def handleFail(self,step,operator):
        self.logger.info("RESULT: %d %s ====>FAIL "%(step+1,operator))
        self.verificationErrors.append("RESULT: %d %s ==>FAIL "%(step+1,operator))
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()