#encoding: utf-8
'''
Created on 2016年12月1日

@author: Jane Wei
'''
#import unittest
import logging
import os, sys
import time
from datetime import datetime
import unittest
from proboscis.asserts import assert_equal
from proboscis.asserts import assert_false
from proboscis.asserts import assert_raises
from proboscis.asserts import assert_true
from proboscis import SkipTest
from proboscis import test
from proboscis import before_class,after_class
from libs.caseObject import caseObject
from libs import logger

@test()
class testLogin():

    #@test(groups='login')
    def testLogin(self):
        caseObject('caseObject\\caseObject.xlsx','pageObject\\pageObject.xlsx').testCase('login')
        
    #@test(groups='search')
    def testSearch(self):
        caseObject('caseObject\\caseObject.xlsx','pageObject\\pageObject.xlsx').testCase('search')
    @test   
    def testApp(self):
        caseObject('caseObject\\caseObject.xlsx','pageObject\\pageObject.xlsx').testCase('apptest')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()