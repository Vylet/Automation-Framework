#encoding: utf-8
'''
Created on 2016年12月13日

@author: Jane Wei
'''
from time import sleep

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
import time
from proboscis.asserts import assert_equal
from proboscis.asserts import assert_false
from proboscis.asserts import assert_raises
from proboscis.asserts import assert_true
from libs.base import Base

class testCase(Base):
    '''
    classdocs
    '''


    def __init__(self, driver):
        '''
        Constructor
        '''
        self.driver = driver
        
    def __delete__(self):
        self.driver.quit()
    
    def calc(self):
        driver = self.driver
        driver.wait_activity('.Calculator', 5)
        print driver.current_activity
        driver.find_element_by_name("1").click()
        driver.find_element_by_name("delete").click()
        print driver.current_activity
        driver.find_element_by_name("5").click()

        driver.find_element_by_name("9").click()

        driver.find_element_by_name("=").click()   