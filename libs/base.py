#coding: utf-8
'''
Created on 2016年12月12日

https://github.com/casschin/appium-pytest/blob/master/screens/screen.py
@author: Jane Wei
'''
from time import sleep
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy as By
#from selenium.webdriver.remote.webelement import WebElement
from libs.logger import logger
from libs.MyException import MyException
from libs.MyException import verificationErrors
import re

class Base(object):

    def __init__(self):
        #self.driver = driver
        self.logger = logger
        self.verificationErrors=verificationErrors

    # get elements
    def get_element(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """
        self.logger.debug('function get_element')
        method = locator.getType()
        values = locator.getSelector()
        self.logger.debug(method)
        self.logger.debug(values)
        if type(values) is str or unicode:
            return self.get_element_by_type(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_element_by_type(method, value)
                except NoSuchElementException:
                    pass
            raise NoSuchElementException

    def get_element_by_type(self, method,value):
        operator = {By.XPATH : self.__xpath,
              By.ID : self.__id, 
              By.NAME : self.__name, #text
              By.ACCESSIBILITY_ID: self.__accessibility_id,
              By.ANDROID_UIAUTOMATOR: self.__android,
              By.IOS_UIAUTOMATION: self.__ios,
              By.CLASS_NAME : self.__className,
              "Other": self.__other,
              }
        return operator.get(method,self.__other)(value)
    
    def __other(self,value):
        raise MyException('Not correctly defined the locator type, please check! "%s"'%value)

    def get_elements(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_elements_by_type(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_elements_by_type(method, value)
                except NoSuchElementException:
                    pass
            raise NoSuchElementException

    def get_elements_by_type(self, method, value):
        if method == 'accessibility_id':
            return self.driver.find_elements_by_accessibility_id(value)
        elif method == 'android':
            return self.driver.find_elements_by_android_uiautomator(value)
        elif method == 'ios':
            return self.driver.find_elements_by_ios_uiautomation(value)
        elif method == 'class_name':
            return self.driver.find_elements_by_class_name(value)
        elif method == 'id':
            return self.driver.find_elements_by_id(value)
        elif method == 'xpath':
            return self.driver.find_elements_by_xpath(value)
        elif method == 'name':
            return self.driver.find_elements_by_name(value)
        else:
            raise Exception('Invalid locator method.')

    # element visible
    def is_visible(self, locator):
        #self.logger.debug('is_visible')
        try:
            self.get_element(locator).is_displayed()
            #WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((locator.getType(), locator.getSelector())))
            #self.logger.debug('after visibility check')
            return True
        except NoSuchElementException:
            return False

    # element present
    def is_present(self, locator):
        try:
            self.get_element(locator)
            return True
        except NoSuchElementException:
            return False

    # waits
    def wait_visible(self, locator, timeout=10):
        #self.logger.debug('wait_visible')
        i = 0
        while i != timeout:
            try:
                self.is_visible(locator)  
                #self.logger.debug('After is_visible')              
                return self.get_element(locator)
            except NoSuchElementException:
                sleep(1)
                i += 1
        raise Exception('Element never became visible: %s (%s)' % (locator[0], locator[1]))

    def wait_for_text(self, locator, text, timeout=10):
        i = 0
        while i != timeout:
            try:
                element = self.get_element(locator)
                element_text = element.text
                if element_text.lower() == text.lower():
                    return True
                else:
                    pass
            except NoSuchElementException:
                pass
            sleep(1)
            i += 1
        raise Exception('Element text never became visible: %s (%s) - %s' % (locator[0], locator[1], text))   

    # gestures
    def swipe_to_element(self, scrollable_element_locator, target_element_locator, direction, duration=None):
        scrollable_element_attributes = self.get_element_attributes(scrollable_element_locator)
        limit = 5
        attempts = 0
        while True:
            if attempts == limit:
                raise Exception('Could not swipe to element')
            if self.is_visible(target_element_locator):
                break
            else:
                if direction == 'up':
                    self.driver.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 1,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 1,
                        duration
                    )
                elif direction == 'down':
                    self.driver.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 1,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 1,
                        duration
                    )
                elif direction == 'left':
                    self.driver.swipe(
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                elif direction == 'right':
                    self.driver.swipe(
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                else:
                    raise Exception('Invalid direction value: %s' % direction)
            attempts += 1

    

    def get_element_attributes(self, locator):
        element = self.get_element(locator)
        return {
            'top': element.location['y'],
            'bottom': element.location['y'] + element.size['height'],
            'left': element.location['x'],
            'right': element.location['x'] + element.size['width'],
            'center_x': (element.size['width']/2) + element.location['x'],
            'center_y': (element.size['height']/2) + element.location['y']
        }

    def pull_to_refresh(self, locator, duration=1000):
        scrollable_element_attributes = self.get_element_attributes(locator)
        self.driver.swipe(
            scrollable_element_attributes['center_x'],
            scrollable_element_attributes['top'] + 1,
            scrollable_element_attributes['center_x'],
            scrollable_element_attributes['bottom'] - 1,
            duration
        )

    def hide_keyboard(self):
        try:
            sleep(1)
            self.driver.hide_keyboard()
        except WebDriverException:
            pass
        
    def getOperation(self,operator,*args,**kw):
        operations={
                'openApp':self.__openApp,
                'click':self.__click,
                'tap': self.__tap,
                'flick':self.__flick,
                'swipe': self.__swipe,
                'hide_keyboard': self.__hide_keyboard,
                'keyevent':self.__keyevent,
                'press_keycode': self.__press_keycode,
                'long_press_keycode': self.__long_press_keycode,
                'drag_and_drop': self.__drag_and_drop,
                'scroll': self.__scroll,
                'pinch': self.__pinch,
                'zoom':self.__zoom,
                'sendKeys': self.__send_keys,
                'clear': self.__clear,
                'reset': self.__reset,
                'shake': self.__shake,
                'open_notifications': self.__open_notifications,
                
                #'getText': self.__getText,
                #'access':self.__access,
                #'hover': self.__hover,
                #'expTitle': self.__verifyTitle,
                #'waitLoading': self.__wait_loading_ready
                }
        return operations.get(operator,self.__click)(*args,**kw)
    
    def __openApp(self,*args,**kw):
        desired_caps = {}
        for item in kw:
            desired_caps[item]=kw[item]
        try:
            self.logger.debug(4)
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            self.logger.debug(5)
            self.driver.implicitly_wait(20)
            #time.sleep(3)
        except Exception,e:
            self.logger.error(e)
            self.verificationErrors.append('__openApp: '+str(e))    
    
    # clicks and taps
    def __click(self, locator):
        try:
            element = self.wait_visible(locator)
            element.click()
        except Exception,e:
            self.logger.error('__click: '+ str(e))
            self.verificationErrors.append('__click: '+ str(e))
    
    def __tap(self,positions,duration): 
        try:
            self.driver.tap(positions, duration)  
        except Exception,e:
            self.logger.error('__tap: '+str(e))
            self.verificationErrors.append('__tap: '+str(e))
    
    #swipe(self, start_x, start_y, end_x, end_y, duration=None)
    def __swipe(self,*args):   
        try:
            self.driver.swipe(args)  
        except Exception,e:
            self.logger.error('__swipe: '+str(e))
            self.verificationErrors.append('__swipe: '+str(e))
            
    def __hide_keyboard(self,*args):
        try:
            self.driver.hide_keyboard(args)
        except Exception,e:
            self.logger.error('__hide_keyboard: '+str(e))
            self.verificationErrors.append('__hide_keyboard: '+str(e))
    
    def __keyevent(self,*args):
        try:
            self.driver.keyevent(args)
        except Exception,e:
            self.logger.error('__keyevent: '+str(e))
            self.verificationErrors.append('__keyevent: '+str(e))  
    
    def __press_keycode(self,*args):
        try:
            self.driver.press_keycode(args)
        except Exception,e:
            self.logger.error('__press_keycode: '+str(e))
            self.verificationErrors.append('__press_keycode: '+str(e))
    def __long_press_keycode(self,*args):
        try:
            self.driver.long_press_keycode(args)
        except Exception,e:
            self.logger.error('__long_press_keycode: '+str(e))
            self.verificationErrors.append('__long_press_keycode: '+str(e))     
    
    def __flick(self,*args):
        try:
            self.driver.flick(args)  
        except Exception,e:
            self.logger.error('__flick: '+str(e))
            self.verificationErrors.append('__flick: '+str(e))
            
    def __drag_and_drop(self,locator1,locator2):
        try:
            elem1 = self.wait_visible(locator1)
            elem2 = self.wait_visible(locator2)
            self.driver.drag_and_drop(elem1, elem2)
        except Exception,e:
            self.logger.error('__drag_and_drop: '+str(e))
            self.verificationErrors.append('__drag_and_drop: '+str(e))
    
    #scroll(self, origin_el, destination_el)        
    def __scroll(self,locator1,locator2):
        try:
            elem1 = self.wait_visible(locator1)
            elem2 = self.wait_visible(locator2)
            self.driver.scroll(elem1, elem2)
        except Exception,e:
            self.logger.error('__scroll: '+str(e))
            self.verificationErrors.append('__scroll: '+str(e))
    
    #pinch(self, element=None, percent=200, steps=50)       
    def __pinch(self,locator=None,percent=200,steps=50):
        try:
            element = self.wait_visible(locator)
            self.driver.pinch(element, percent, steps)
        except Exception,e:
            self.logger.error('__pinch: '+str(e))
            self.verificationErrors.append('__pinch: '+str(e))
            
    def __zoom(self,locator=None, percent=200, steps=50):
        try:
            element = self.wait_visible(locator)
            self.driver.zoom(element, percent, steps)
        except Exception,e:
            self.logger.error('__zoom: '+str(e))
            self.verificationErrors.append('__zoom: '+str(e))
        
               
    # send keys
    def __send_keys(self, locator, text):
        try:
            element = self.wait_visible(locator)
            element.send_keys(text)
        except Exception,e:
            self.logger.error('__send_keys: '+str(e))
            self.verificationErrors.append('__send_keys: '+str(e))
            
    def __clear(self,locator): 
        try:
            element = self.wait_visible(locator)
            element.clear()
        except Exception,e:
            self.logger.error('__clear:' + str(e))
            self.verificationErrors.append('__clear:' + str(e)) 
            
    def __reset(self):
        try:
            self.driver.reset()
        except Exception,e:
            self.logger.error('__reset:' + str(e))
            self.verificationErrors.append('__reset:' + str(e)) 
    
    def __shake(self):
        try:
            self.driver.shake()
        except Exception,e:
            self.logger.error('__shake:' + str(e))
            self.verificationErrors.append('__shake:' + str(e))
    
    def __open_notifications(self):
        try:
            self.driver.open_notifications()
        except Exception,e:
            self.logger.error('__open_notifications:' + str(e))
            self.verificationErrors.append('__open_notifications:' + str(e))
            
    def __long_press(self, locator, duration=1000):
        try:
            element = self.get_element(locator)
            action = TouchAction(self.driver)
            action.long_press(element, None, None, duration).perform()
        except Exception,e:
            self.logger.error('__long_press:' + str(e))
            self.verificationErrors.append('__long_press:' + str(e)) 

    '''    
    def __getText(self,locator):
        elem = self.get_element_by_type(locator.getType(),locator.getSelector())
        return elem.get_text()
    
    def __getAttribute(self,locator,attr):
        elem = self.get_element_by_type(locator.getType(),locator.getSelector())
        return elem.get_attribute(attr)
    
    def __access(self,address):
        self.driver.get(address) 
        
    def __verifyTitle(self,title):
        t = self.driver.title
        #self.logger.info("current page title: "+t)
        if t == title:
            return True
        else:
            #print("Page title is not as expect, expect to '%s' , actual '%s'"%(title,t))
            self.verificationErrors.append("Page title is not as expect, expect to '%s' , actual '%s'"%(title,t))
            self.logger.error("Page title is not as expect, expect to '%s' , actual '%s'"%(title,t))
            return False
    
    def __hover(self,locator):
        #self.logger.info("hover")
        elem = self.get_element_by_type(locator.getType(),locator.getSelector())
        #self.logger.info (elem)
        ActionChains(self.driver).move_to_element(elem).perform()
        
    def __wait_loading_ready(self):
        js_script="return (document.readyState == 'complete' && jQuery.active == 0)"
        i=0
        while (i<60):
            if self.driver.execute_script(js_script):   
                break
            else:
                time.sleep(1)
                i+=1
        
        assert_true(i<60,"Waiting script loading more than 60 times")'''
    
    #resource-id
    def __id(self,value):
        #self.logger.debug('by id: "%s"'%value)
        try:
            e = self.driver.find_element_by_id(value)
            return e
        except Exception, e:
            self.logger.error('__id: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False
    
    #appium text
    def __name(self,value):
        try:
            e = self.driver.find_element_by_name(value)
            return e
        except Exception, e:
            self.logger.error('__name: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False
    
    def __tagName(self,value):
        try:
            e = self.driver.find_element_by_tag_name(value)
            return e
        except Exception, e:
            self.logger.error('__tagName: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False
    
    #class
    def __className(self,value):
        try:
            e=self.driver.find_element_by_class_name(value)
            return e
        except Exception, e:
            self.logger.error('__className: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False
    
    def __accessibility_id(self,value):
        #self.logger.debug('content-desc: "%s"'%value)
        try:
            e = self.driver.find_element_by_accessibility_id(value)
            return e
        except Exception, e:
            self.logger.error('__accessibility_id: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False

    def __linkText(self,value):
        e = self.driver.find_element_by_link_text(value)
        return e

    def __cssSelector(self,value):
        e = self.driver.find_element_by_css_selector(value)
        return e
    
    def __xpath(self,value):
        #self.logger.debug('by xpath: "%s"'%value)
        try:
            e = self.driver.find_element_by_xpath(value)
            return e
        except Exception, e:
            self.logger.error('__xpath: Not get the element "%s" detail: "%s"'%(value,str(e)))
            return False
    
    def __partialLinkText(self,value):
        e = self.driver.find_element_by_partial_link_text(value)
        return e
    
    def __scriptJS(self,value):
        e = self.driver.execute_script(value)
        return e
    
    def __android(self,value):        
        e = self.driver.find_element_by_android_uiautomator('new UiSelector().%s' % value)
        return e 
    
    def __ios(self,value):
        e = self.driver.find_element_by_ios_uiautomation(value)
        return e  
    
    
    def verify(self,operator,*args,**kw):
    #def verify(self,operator):
        operations ={
                    'verify_true': self.__verify_true,
                   'verify_false': self.__verify_false,
                   'verify_equal': self.__verify_equal,
                   'verify_not_equal': self.__verify_not_equal,
                   'verify_match': self.__verify_match,
                   'verify_not_match': self.__verify_not_match,
                   'verify_in': self.__verify_in,
                   'verify_not_in': self.__verify_not_in,
                   
                   }
        return operations.get(operator)(*args,**kw)
        #return operations.get(operator)
    
    def __verify_true(self, locator,attribute,*args):
        #self.logger.debug('__verify_true') 
        #self.logger.debug(attribute)
        try:
            elem = self.wait_visible(locator)
            if callable(getattr(elem,attribute)):
                #self.logger.debug('callable')
                return getattr(elem,attribute)()
            else:
                #self.logger.debug('not callable')
                return getattr(elem,attribute)
        except Exception,e:
            self.logger.error('__verify_true: '+str(e))
            self.verificationErrors.append('__verify_true: '+str(e)) 
            
    def __verify_false(self, locator,attribute,*args):
        #self.logger.debug('__verify_false') 
        #self.logger.debug(attribute)
        try:
            elem = self.wait_visible(locator)
            if callable(getattr(elem,attribute)):
                #self.logger.debug('callable')
                #self.logger.debug(getattr(elem,attribute)())
                return not getattr(elem,attribute)()
            else:
                #self.logger.debug('not callable')
                #self.logger.debug(getattr(elem,attribute))
                return not getattr(elem,attribute)
        except Exception,e:
            self.logger.error('__verify_false: '+str(e))
            self.verificationErrors.append('__verify_false: '+str(e)) 
            
    def __verify_equal(self,locator,attribute,expectResult):
        return self.__equal(locator, attribute, expectResult, True)
    
    def __verify_not_equal(self,locator,attribute,expectResult):
        return self.__equal(locator, attribute, expectResult, False)
        
    def __equal(self,locator,attribute,expectResult,exp=True):
        try:
            elem = self.wait_visible(locator)
            if not elem:
                self.logger.info('Not find the element %s'%locator)
                return False 
            if callable(getattr(elem,attribute)):
                act = getattr(elem,attribute)()
            else:
                act = getattr(elem,attribute)
            self.logger.info('Actual: "%s" type: "%s"'%(act,type(act)) )
            self.logger.info('Expect: "%s" type: "%s"'%(expectResult,type(expectResult)) ) 
            #self.logger.debug(unicode(expectResult)==unicode(act))
            #self.logger.debug(expectResult==act)
            if exp:
                return expectResult==act
            else:
                return not expectResult==act
            #return expectResult==act if exp else not unicode(expectResult)==unicode(act)
        except Exception,e:
            self.logger.error('__verify_equal: '+str(e))
            self.verificationErrors.append('__verify_equal: '+str(e)) 
            
    def __verify_match(self,locator,attribute,matchPattern):
        self.__match(locator, attribute, matchPattern, True)
    
    def __verify_not_match(self,locator,attribute,matchPattern):
        self.__match(locator, attribute, matchPattern, False)
        
    def __match(self,locator,attribute,matchPattern,exp=True):
        try:
            elem = self.wait_visible(locator)
            if callable(getattr(elem,attribute)):   
                result = getattr(elem,attribute)()
            else:
                result = getattr(elem,attribute)
            return re.search(re.escape(matchPattern),result) if exp else not re.search(matchPattern,result)
        
        except Exception,e:
            self.logger.error('__match: '+str(e))
            self.verificationErrors.append('__match: '+str(e)) 
            
    def __verify_in(self, locator,attribute, expmember):
        self.__in(locator, attribute, expmember, True)
    
    def __verify_not_in(self, locator,attribute, expmember):
        self.__in(locator, attribute, expmember, False)
        
    def __in(self, locator,attribute, expmember, exp=True):
        try:
            elem = self.wait_visible(locator)
            if callable(getattr(elem,attribute)):   
                container = getattr(elem,attribute)()
            else:
                container = getattr(elem,attribute)
            return expmember in container if exp else expmember not in container
        
        except Exception,e:
            self.logger.error('__verify_equal: '+str(e))
            self.verificationErrors.append('__verify_equal: '+str(e)) 

        
    def str2Dict(self,s):
        arg = {}
        y=s.split(',')
        for i in y:
            j=i.split(':')
            arg[j[0]] = j[1]
        return arg
        '''arg2 = '{"'+step[6]+'"}'
                    arg2 = arg2.replace(',','","')
                    arg2 = arg2.replace(':','":"')
                    arg2 = json.loads(arg2)'''