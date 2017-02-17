#! /usr/bin/python
# coding:utf-8

import time
try:
    import cmd2 as cmd
except ImportError:
    import cmd
import os
import sys
from tools.configs import *
from tools.run import *
from tools.check import *
from tools.save import *

class VRLT(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "(VRLT)>"
        self.intro = '''简要说明：通过以下命令, 运行指定的漏洞程序
        load                      加载程序
        show v                    显示可以利用的漏洞程序
        show report               显示运行程序之后产生的报告
        save report               保存运行程序之后产生的报告
        clear report              清空报告内容
        select i                  选择第i个要执行的程序
        select i1 i2 ...          选择第i1,i2,i3...个要执行的程序
        select all                选择所有的程序执行
        run                       运行选择的漏洞程序,并进行攻击
        run normal                运行选择的漏洞程序,正常运行
        attach i                  附加调试第i个程序
        aslr status               获取ASLR的状态
        aslr on/off/conservative  修改ASLR状态'''
        self.run_name = []

    def do_load(self, line):
        global program_names
        program_names = []
        config_base_path()
        config_report_path()
        config_attach_false()
        config_normal_false()
        base_path = os.environ["BASE_PATH"]
        for name in os.listdir(base_path):
            if check_difine_standard(name):
                program_names.append(str(name))


    def do_show(self, line):
        if line == 'v':
            i = 1
            if len(program_names) == 0:
                print 'Do not have program!!!'
            else:
                for name in program_names:
                    print str(i) + ': ' + name
                    i = i + 1
        elif line == 'report':
            if len(check_result)==0:
                print 'no report'
                return
            for ret in check_result:
                print ret
        else:
            print 'command error!!!'

    def do_save(self, line):
        if line=='report':
            if len(check_result) == 0:
                print 'no report'
                return
            save_report()
        else:
            print 'command error'

    def do_clear(self, line):
        if line=='report':
            clear_report()
        else:
            print 'command error'




    def do_select(self, line):
        self.run_name = []
        if line == 'all':
            for name in program_names:
                self.run_name.append(name)
            return
        program_nums = line.split()
        for program_num in program_nums:
            try:
                num = int(program_num)
                if num > len(program_names):
                    print 'select error,please reselect'
                    return
                else:
                    self.run_name.append(program_names[int(program_num) - 1])
            except:
                print 'please input correct number to select vulnerability'
                return



    def do_run(self, line):
        if len(self.run_name) == 0:
            print 'please select vulnerability!!!'
            return
        if len(line) == 0:
            config_normal_false()
            run(self.run_name)
        elif line == 'normal':
            config_normal_true()
            run_normal(self.run_name)
        else:
            print 'command error!!!'

    def do_aslr(self, line):
        '''Check status/Turn on/Turn off ASLR of system.
Format: aslr status/frame_check/on/off/conservative'''
        if line in ['status', 'on', 'off', 'conservative']:
            if line[1] == 't':
                state = aslr_status()
                if state == 2:
                    print "ASLR: ON\n"
                elif state == 0:
                    print "ASLR: OFF\n"
                elif state == 1:
                    print "ASLR: Conservative ON\n"
                else:
                    print "Invalid Value."
            elif line[1] == 'n':
                aslr_on()
            elif line[1] == 'f':
                aslr_off()
            elif line[1] == 'o':
                aslr_conservative()
        else:
            print 'command error!!!'

    def do_attach(self,line):
        if len(program_names) == 0:
            print 'Do not have program!!!'
            return
        try:
            num = int(line)
            if num > len(program_names):
                print 'select error,please reselect'
                return
        except:
            print 'please input correct number to select vulnerability'
            return
        config_attach_true()
        names = []
        names.append(program_names[num-1])
        run(names)
        pids = pidof(program_names[num-1])
        pid = max(pids)
        gdb(file_name=program_names[num-1], pid=pid)
        config_attach_false()

    def help_com(self):

        print "\
        load                      加载程序\n\
        show v                    显示可以利用的漏洞程序\n\
        show report               显示运行程序之后产生的报告\n\
        save report               保存运行程序之后产生的报告\n\
        clear report              清空报告内容\n\
        select i                  选择第i个要执行的程序\n\
        select i1 i2 ...          选择第i1,i2,i3...个要执行的程序\n\
        select all                选择所有的程序执行\n\
        run                       运行选择的漏洞程序,并进行攻击\n\
        run normal                运行选择的漏洞程序,正常运行\n\
        attach i                  附加调试第i个程序\n\
        aslr status               获取ASLR的状态\n\
        aslr on/off/conservative  修改ASLR状态\n\
        q                         退出\n"





if __name__=='__main__':
    vrlt = VRLT()
    vrlt.do_load('')
    vrlt.cmdloop()
