#! /usr/bin/python
#coding:utf-8
import os
from ctypes import *
global check_result
check_result = []

def check(name):
    check_name = os.environ['CHECK_' + name + '_PATH'] + '.so'
    lib = cdll.LoadLibrary(check_name)
    lib.check.restype = c_char_p
    res = lib.check()
    check_result.append(res)

def check_file(path, name, postfixs):
    flag = 0
    if len(postfixs)==0:
        if (not os.path.exists(os.path.abspath(os.path.join(path, name)))):
            return False
        else:
            flag = 1
    for postfix in postfixs:
        file_name = name + postfix
        if (os.path.exists(os.path.abspath(os.path.join(path, file_name)))):
            flag = 1
            break
    if flag == 0:
        return False
    return True

def check_difine_standard(name):
    name_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name))
    vul_path = os.path.abspath(os.path.join(name_path, 'vulnerabilities'))
    check_path = os.path.abspath(os.path.join(name_path, 'check'))
    input_path = os.path.abspath(os.path.join(name_path, 'input'))
    output_path = os.path.abspath(os.path.join(name_path, 'output'))
    document_path = os.path.abspath(os.path.join(name_path, 'document'))
    if (not os.path.exists(vul_path)) | (not os.path.exists(check_path)) | (not os.path.exists(input_path)) | (not os.path.exists(output_path)) | (not os.path.exists(document_path)):
        return False
    postfixs = []
    if not check_file(vul_path, name, postfixs):
        return False
    postfixs = ['.so']
    if not check_file(check_path, name, postfixs):
        return False
    postfixs = ['.txt']
    if not check_file(input_path, name, postfixs):
        return False
    ''' postfixs = ['.txt']
    if not check_file(output_path, name, postfixs):
        print '5'
        return False'''
    postfixs = ['.docx']
    if not check_file(document_path, name, postfixs):
        return False
    return True





