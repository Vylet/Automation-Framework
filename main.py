#coding: utf-8
'''
Created on 2016年11月30日

@author: Jane Wei
'''

import os
from datetime import datetime
import codecs
import sys
import HTMLTestRunner
from libs.logger import REPORT_FILE

def run_tests(test_report_file):
    from proboscis import TestProgram
    from Tests import testLogin

    try:
        #TestProgram().run_and_exit()
        with codecs.open(test_report_file,mode='wb',encoding='UTF-8') as fp:
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='TEST REPORT',description='Test Cases running results as following:')
            runner.run(TestProgram().test_suite)
    except SystemExit:
        os._exit(0)


if __name__ == '__main__':
    run_tests(REPORT_FILE)