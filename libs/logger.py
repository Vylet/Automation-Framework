#coding: utf-8
'''
Created on 2016��12��2

@author: Jane Wei
'''

import logging
import os
import sys
from datetime import datetime
import HTMLTestRunner

def setup_file_logger(logger_name, log_file,show_in_console=True, level=logging.DEBUG):

    l = logging.getLogger(logger_name)
    l.setLevel(level)

    # Create the handlers
    logFileHandler = logging.FileHandler(log_file)
    reportFileHandler = logging.StreamHandler(HTMLTestRunner.stdout_redirector)
    consolehandler = logging.StreamHandler()

    #config the formatter
    formatter = logging.Formatter('%(asctime)s - {%(module)s} - line[%(lineno)d] - %(levelname)s :%(message)s')
    
    formatter2 = logging.Formatter('{%(module)s}-line[%(lineno)d]: %(message)s')

    #Config the handlers with the formatter and the level to report
    logFileHandler.setFormatter(formatter)
    logFileHandler.setLevel(level=level)
    
    reportFileHandler.setFormatter(formatter2)
    reportFileHandler.setLevel(level=logging.INFO)

    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(level=level)

    l.addHandler(logFileHandler)
    l.addHandler(reportFileHandler)
    if show_in_console == True:
        l.addHandler(consolehandler)

    l.info("Logger set up...")

nowstamp = datetime.now()
timeNow = datetime.time(nowstamp)
dateNow = datetime.date(nowstamp)

#os.getcwd()
LOG_FILE = os.getcwd() + '/logs/testlog_' + '{year}{month:02}{day:02}_{hour:02}{minute:02}'.format(year=dateNow.year, month=dateNow.month, day=dateNow.day, hour=timeNow.hour, minute=timeNow.minute) + '.log'
REPORT_FILE = os.getcwd()+'/report/testreport_'+'{year}{month:02}{day:02}_{hour:02}{minute:02}'.format(year=dateNow.year, month=dateNow.month, day=dateNow.day, hour=timeNow.hour, minute=timeNow.minute)+'.html'

setup_file_logger('console_log',LOG_FILE,True)
logger = logging.getLogger('console_log')
