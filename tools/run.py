#! /usr/bin/python
#coding:utf-8
import os
from tools.configs import *
from tools.check import *
from tools.save import *

def config_path(name):
    config_vul_path(name)
    config_check_path(name)
    config_output_path(name)
    config_input_path(name)
    config_document_path(name)

def run(names):
    for name in names:
        config_path(name)
        if aslr_infos[name] == 'on':
            aslr_on()
        elif aslr_infos[name] == 'off':
            aslr_off()
        else:
            print name + ' aslr config error !!!'
            break
        environ_name = 'VUL_' + name + '_PATH'
        chang_path(environ_name)
        output_name = os.environ['OUTPUT_' + name + '_PATH'] + '.txt'
        if os.path.exists(output_name):
            os.remove(output_name)
        path = os.environ['VUL_' + name + '_PATH']
        command = new_terminal(path)#"gnome-terminal -e 'bash -c \"" + path + "; exec bash\"'"
        os.popen(command)
        remove_path(environ_name)
        check(name)


def run_normal(names):
    for name in names:
        config_path(name)
        if aslr_infos[name] == 'on':
            aslr_on()
        elif aslr_infos[name] == 'off':
            aslr_off()
        else:
            print name + ' aslr config error !!!'
            break
        environ_name = 'VUL_' + name + '_PATH'
        chang_path(environ_name)
        path = os.environ['VUL_' + name + '_PATH']
        command = new_terminal(path)#"gnome-terminal -e 'bash -c \"" + path + "; exec bash\"'"
        os.popen(command)
        remove_path(environ_name)
