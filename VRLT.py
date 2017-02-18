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
        show p                    显示可以利用的所有程序
        show v                    按漏洞程序的类型进行划分显示
        show e                    按攻击程序的类型进行划分显示
        cat report name           查看产生的报告，默认查看report.txt，可指定报告的名字
        save report name          保存产生的报告，默认保存为report.txt，可指定报告的名字
        del report name           删除产生的报告，默认删除report.txt，可指定报告的名字
        select i                  选择第i个要执行的程序
        select i1 i2 ...          选择第i1,i2,i3...个要执行的程序
        select all                选择所有的程序执行
        select v type             选择type类型的漏洞程序
        select e type             选择type类型的攻击程序
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
        get_config_info(program_names)
        get_v_info(program_names)
        get_e_info(program_names)
        get_aslr_info(program_names)
        get_compile_info(program_names)


    def do_show(self, line):
        if line == 'p':
            i = 1
            if len(program_names) == 0:
                print 'Do not have program!!!'
            else:
                for name in program_names:
                    print str(i) + ': ' + name
                    i = i + 1
        elif line == 'v':
            i = 1
            for vul_type in v_infos.keys():
                print str(i) + ': ' + vul_type
                i = i + 1
        elif line == 'e':
            i = 1
            for e_type in e_infos.keys():
                print str(i) + ': ' + e_type
                i = i + 1
        else:
            print 'command error!!!'

    def do_save(self, line):
        length = len(line.split())
        if length > 0:
            if line.split()[0]=='report':
                if length > 1:
                    save_report(line.split()[1])
                else:
                    save_report()
            else:
                print 'command error'
        else:
            print 'command error'

    def do_select(self, line):
        self.run_name = []
        if len(line) == 0:
            print 'select error,please reselect'
            return
        if line == 'all':
            for name in program_names:
                self.run_name.append(name)
            return
        elif line.split()[0] == 'v':
            if(len(line.split())<2):
                print 'select error,please reselect'
                return
            if v_infos.has_key(line.split()[1]):
                program_nums = v_infos[line.split()[1]]
            else:
                print 'select error,please reselect'
                return
        elif line.split()[0] == 'e':
            if (len(line.split()) < 2):
                print 'select error,please reselect'
                return
            if e_infos.has_key(line.split()[1]):
                program_nums = e_infos[line.split()[1]]
            else:
                print 'select error,please reselect'
                return
        else:
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
            generator_report()
            clear_check_result()
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

    def do_cat(self,line):
        length = len(line.split())
        if length > 0:
            if line.split()[0] == 'report':
                if length > 1:
                    infos = cat_report(line.split()[1])
                else:
                    infos = cat_report()
                for info in infos:
                    print info
            else:
                print 'command error'
        else:
            print 'command error'

    def do_del(self,line):
        length = len(line.split())
        if length > 0:
            if line.split()[0] == 'report':
                if length > 1:
                    del_report(line.split()[1])
                else:
                    del_report()
            else:
                print 'command error'
        else:
            print 'command error'

    def help_run(self):

        print "\
        load                      加载程序\n\
        show v                    显示可以利用的漏洞程序\n\
        show report               显示运行程序之后产生的报告\n\
        cat report                查看保存的报告\n\
        clear report              清空报告内容\n\
        del report                删除保存的报告\n\
        select i                  选择第i个要执行的程序\n\
        select i1 i2 ...          选择第i1,i2,i3...个要执行的程序\n\
        select all                选择所有的程序执行\n\
        select v type             选择type类型的漏洞程序\n\
        select e type             选择type类型的攻击程序\n\
        run                       运行选择的漏洞程序,并进行攻击\n\
        run normal                运行选择的漏洞程序,正常运行\n\
        attach i                  附加调试第i个程序\n\
        aslr status               获取ASLR的状态\n\
        aslr on/off/conservative  修改ASLR状态\n\
        q                         退出\n"





if __name__=='__main__':
    os.system('clear')
    vrlt = VRLT()
    vrlt.do_load('')
    vrlt.cmdloop()
