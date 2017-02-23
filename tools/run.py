#! /usr/bin/python
#coding:utf-8
import os
import tools.configs
import tools.check


def config_path(name):
    tools.configs.config_vul_path(name)
    tools.configs.config_check_path(name)
    tools.configs.config_output_path(name)
    tools.configs.config_input_path(name)
    tools.configs.config_document_path(name)

def run(names):
    for name in names:
        config_path(name)
        if tools.configs.aslr_infos[name] == 'on':
            tools.configs.aslr_on()
        elif tools.configs.aslr_infos[name] == 'off':
            tools.configs.aslr_off()
        else:
            print name + ' aslr config error !!!'
            break
        environ_name = 'VUL_' + name + '_PATH'
        tools.configs.chang_path(environ_name)
        output_name = os.environ['OUTPUT_' + name + '_PATH'] + '.txt'
        if os.path.exists(output_name):
            os.remove(output_name)
        path = os.environ['VUL_' + name + '_PATH']
        command = tools.configs.new_terminal(path)#"gnome-terminal -e 'bash -c \"" + path + "; exec bash\"'"
        os.popen(command)
        tools.configs.remove_path(environ_name)
        tools.check.check(name)


def run_normal(names):
    for name in names:
        config_path(name)
        if tools.configs.aslr_infos[name] == 'on':
            tools.configs.aslr_on()
        elif tools.configs.aslr_infos[name] == 'off':
            tools.configs.aslr_off()
        else:
            print name + ' aslr config error !!!'
            break
        environ_name = 'VUL_' + name + '_PATH'
        tools.configs.chang_path(environ_name)
        path = os.environ['VUL_' + name + '_PATH']
        command = tools.configs.new_terminal(path)#"gnome-terminal -e 'bash -c \"" + path + "; exec bash\"'"
        os.popen(command)
        tools.configs.remove_path(environ_name)
