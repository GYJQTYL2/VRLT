#! /usr/bin/python
#coding:utf-8
import os
import subprocess
import shutil
import time
import tools.check

attack_fail_nums = 0
attack_success_nums = 0

def save_report(report_name='report.txt'):
    src_file_name = os.path.abspath(os.path.join(os.environ["REPORT_PATH"], 'report.txt'))
    if not os.path.exists(src_file_name):
        print 'Do not have report to save !!! '
    des_file_name = os.path.abspath(os.path.join(os.environ["REPORT_PATH"], report_name))
    shutil.copy(src_file_name,des_file_name)

def del_report(del_report_name='report.txt'):
    report_name = os.environ["REPORT_PATH"] + '/' + del_report_name
    if os.path.exists(report_name):
        os.remove(report_name)
    else:
        print 'Do not have ' + del_report_name + ' to delete !!!'

def cat_report(cat_report_name='report.txt'):
    report_name = os.environ["REPORT_PATH"] + '/' + cat_report_name
    if os.path.exists(report_name):
        p = subprocess.Popen(r"cat " + str(report_name), stdout=subprocess.PIPE, shell=True)
        lst = p.stdout.read().split('\n')
        return lst
    else:
        lst = []
        lst.append("Do not have " + cat_report_name +" to display!!!")
        return lst

def generator_report():
    global attack_fail_nums
    global attack_success_nums
    attack_fail_info = {}
    attack_success_info = {}
    for res in tools.check.check_result.keys():
        if tools.check.check_result[res].split(',')[0] == 'attack fail':
            attack_fail_nums += 1
            attack_fail_info[res] = tools.check.check_result[res]
        else:
            attack_success_nums += 1
            attack_success_info[res] = tools.check.check_result[res]
    file_name = os.path.abspath(os.path.join(os.environ["REPORT_PATH"], 'report.txt'))
    fp = open(file_name, 'w')
    fpl = open(os.path.abspath(os.path.join(os.environ["REPORT_PATH"], 'log.txt')), 'a')
    fpl.write(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())) + '\n')
    info = 'attack fail numbers:' + str(attack_fail_nums) + "\n"
    fp.write(info)
    fpl.write(info)
    info = 'attack success numbers:' + str(attack_success_nums) + "\ndetail infomation: \n"
    fp.write(info)
    fpl.write(info)
    info = 'attack fail program: \n'
    fp.write(info)
    fpl.write(info)
    for ret in attack_fail_info.keys():
        info = ret + ": " + attack_fail_info[ret] + '\n'
        fp.write(info)
        fpl.write(info)
    info = 'attack success program: \n'
    fp.write(info)
    fpl.write(info)
    for ret in attack_success_info.keys():
        info = ret + ": " + attack_success_info[ret] + '\n'
        fp.write(info)
        fpl.write(info)
    fp.close()
    fpl.close()
    attack_fail_nums = 0
    attack_success_nums = 0

