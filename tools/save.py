#! /usr/bin/python
#coding:utf-8
import os
from tools.check import *

def save_report():
    file_name = os.path.abspath(os.path.join(os.environ["REPORT_PATH"], 'report.txt'))
    fp = open(file_name, 'w')
    for ret in check_result:
        info = ret + "\n"
        fp.write(info)
    fp.close()

def clear_report():
    check_result[:] = []
    report_name = os.environ["REPORT_PATH"] + '/report.txt'
    if os.path.exists(report_name):
        os.remove(report_name)