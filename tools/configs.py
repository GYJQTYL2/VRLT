#! /usr/bin/python
#coding:utf-8
import os
import subprocess
import sys
c_config_infos = {}
v_infos = {}
e_infos = {}
aslr_infos = {}
compile_infos = {}
def config_base_path():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'src'))
    os.environ["BASE_PATH"] = base_path


def config_vul_path(name):
    vul_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name, 'vulnerabilities', name))
    environ_name = 'VUL_' + name + '_PATH'
    os.environ[environ_name] = vul_path


def config_check_path(name):
    check_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'check', name))
    environ_name = 'CHECK_' + name + '_PATH'
    os.environ[environ_name] = check_path


def config_output_path(name):
    output_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'output', name))
    environ_name = 'OUTPUT_' + name + '_PATH'
    os.environ[environ_name] = output_path


def config_input_path(name):
    input_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'input', name))
    environ_name = 'INPUT_' + name + '_PATH'
    os.environ[environ_name] = input_path


def config_document_path(name):
    document_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'document', name))
    environ_name = 'DUCUMENT_' + name + '_PATH'
    os.environ[environ_name] = document_path

def config_report_path():
    report_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"],  'report'))
    environ_name = 'REPORT_PATH'
    os.environ[environ_name] = report_path

def config_config_path(name):
    config_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'Config'))
    environ_name = 'CONFIG' + name + '_PATH'
    os.environ[environ_name] = config_path

def config_normal_true():
    environ_name = 'NORMAL'
    os.environ[environ_name] = "TRUE"

def config_normal_false():
    environ_name = 'NORMAL'
    os.environ[environ_name] = "FALSE"


def config_attach_true():
    environ_name = 'ATTACH'
    os.environ[environ_name] = "TRUE"


def config_attach_false():
    environ_name = 'ATTACH'
    os.environ[environ_name] = "FALSE"


def aslr_status():
    p = subprocess.Popen("cat /proc/sys/kernel/randomize_va_space", stdout=subprocess.PIPE, shell=True)
    ans = p.stdout.read()
    return int(ans[0])

def aslr_on():
    if aslr_status() == 2:
        print 'ASLR is already ON\n'
        return
    print 'ASLR>>ON, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=2", stdin=subprocess.PIPE, shell=True)
    p.wait()

def aslr_off():
    if aslr_status() == 0:
        print 'ASLR is already OFF\n'
        return
    print 'ASLR>>OFF, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=0", stdin=subprocess.PIPE, shell=True)
    p.wait()

def aslr_conservative():
    if aslr_status() == 1:
        print 'ASLR is already Conservative\n'
        return
    print 'ASLR>>Conservative, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=1", stdin=subprocess.PIPE, shell=True)
    p.wait()

def new_terminal(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, leave in the terminal.'''
    cmd_bash = command + '; exec bash'
    e_command = "'bash -c \""+cmd_bash+"\"'"
    return "gnome-terminal -e "+e_command

def new_terminal_exit(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, exit the terminal.'''
    return "gnome-terminal -e '"+command+"'"

def chang_path(environ_name):
    path = os.path.abspath(os.path.join(os.environ[environ_name],os.path.pardir))
    os.chdir(path)
    sys.path.append(path)

def remove_path(environ_name):
    path = os.path.abspath(os.path.join(os.environ[environ_name],os.path.pardir))
    sys.path.remove(path)
    os.chdir(sys.path[0])

def pidof(file_name):
    '''Same as bash, return a list of pid number.'''
    p = subprocess.Popen(r"pidof " + str(file_name), stdout=subprocess.PIPE, shell= True)
    lst = p.stdout.read().split()
    lst = [int(i) for i in lst]
    return lst

def gdb(file_name='',pid=0, sudo=True):
    '''Open a gdb.'''
    cmd = ''
    if sudo: cmd += 'sudo '
    cmd += 'gdb '
    if file_name: cmd += file_name + ' ' + str(pid)
    environ_name = 'VUL_' + file_name + '_PATH'
    chang_path(environ_name)
    os.system(new_terminal_exit(cmd))
    remove_path(environ_name)

def get_config_info(names):
    for name in names:
        config_path = os.path.abspath(os.path.join(os.environ["BASE_PATH"], name,  'Config'))
        fp = open(config_path, 'r')
        config_infos = fp.read().split('\n')
        c_config_infos[name] = {}
        for config_info in config_infos:
            if len(config_info.split('='))==2:
                c_config_infos[name][config_info.split('=')[0]] = config_info.split('=')[1]
        fp.close()

def get_v_info(names):
    for name in names:
        if(not v_infos.has_key(c_config_infos[name]['vul_type'])):
            v_infos[c_config_infos[name]['vul_type']] = []
        v_infos[c_config_infos[name]['vul_type']].append(names.index(name)+1)

def get_e_info(names):
    for name in names:
        if (not e_infos.has_key(c_config_infos[name]['attack_type'])):
            e_infos[c_config_infos[name]['attack_type']] = []
        e_infos[c_config_infos[name]['attack_type']].append(names.index(name)+1)

def get_aslr_info(names):
    for name in names:
        aslr_infos[name] = c_config_infos[name]['aslr']

def get_compile_info(names):
    for name in names:
        compile_infos[name] = c_config_infos[name]['compile']




















