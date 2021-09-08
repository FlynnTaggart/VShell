import zipfile
import sys
import signal
import os
import shutil
import platform
from datetime import datetime, timezone
from termcolor import colored

user_os = platform.system()

input_path = sys.argv[1]

archive = zipfile.ZipFile(input_path)
vshell_root_dir = os.getcwd()
if user_os == 'Windows':
    vshell_root_dir = vshell_root_dir.replace('\\', '/')

try:
    os.mkdir('temporary_files')
except FileExistsError:
    shutil.rmtree('temporary_files')
    os.mkdir('temporary_files')
os.chdir('temporary_files')

archive.extractall()

def custom_split(input_list):
    splitted = []
    temp_str = ''
    i = 0
    while True:
        if i >= len(input_list):
            break
        if input_list[i][0] == '\'':
            cnt = 0
            for j in range(i, len(input_list)):
                if input_list[j][len(input_list[j]) - 1] == '\'':
                    temp_str += input_list[j]
                    splitted.append(temp_str[1:len(temp_str) - 1])
                    cnt += 1
                    break
                temp_str += input_list[j] + ' '
                cnt += 1
            i += cnt
        else:
            splitted.append(input_list[i])
        i += 1
    return splitted

# Exiting and Ctrl + C handling
def exit(signal, frame):
    os.chdir(vshell_root_dir)
    try:
        shutil.rmtree('temporary_files')
    except Exception:
        pass
    print(colored('\nExiting VShell...', 'green'))
    sys.exit(0)

signal.signal(signal.SIGINT, exit)

def pwd():
    current_dir = os.getcwd()
    if user_os == 'Windows':
        current_dir = current_dir.replace('\\', '/')
    print(current_dir[len(vshell_root_dir + '/temporary_files'):] + '/')
    return

def pwd_str():
    current_dir = os.getcwd()
    if user_os == 'Windows':
        current_dir = current_dir.replace('\\', '/')
    str = current_dir[len(vshell_root_dir + '/temporary_files'):] + '/'
    return str

def cd(input_list):
    if len(input_list) == 1:
        return
    change_dir_list = input_list[1].split('/')
    for i in range(len(change_dir_list)):
        if change_dir_list[i] == '' and i == 0:
            os.chdir(vshell_root_dir + '/temporary_files')
            continue
        elif change_dir_list[i] == '':
            continue
        elif change_dir_list[i] == '..' and pwd_str() == '/':
            continue
        try:
            os.chdir(change_dir_list[i])
        except NotADirectoryError:
            print('cd: ' + input_list[1] + ': Not a directory')
            break
        except OSError:
            print('cd: ' + input_list[1] + ': No such file or directory')
            break
    return

def cat(input_list):

    return

def ls(input_list):
    if len(input_list) == 1:
        for cur_dir in os.scandir():
            cur_dir_name = cur_dir.name
            if ' ' in cur_dir_name:
                cur_dir_name = '\'{0}\''.format(cur_dir_name)
            if cur_dir.is_dir():
                print(colored(cur_dir_name, 'blue'))
            else:
                print(cur_dir_name)
    elif len(input_list) == 2:
        if input_list[1] == '-l':
            for cur_dir in os.scandir():
                seconds_date = cur_dir.stat().st_mtime
                date = datetime.fromtimestamp(seconds_date, tz=None)
                cur_dir_name = cur_dir.name
                if ' ' in cur_dir_name:
                    cur_dir_name = '\'{0}\''.format(cur_dir_name)
                if cur_dir.is_dir():
                    print('           ' + date.strftime('%Y %b %d %H:%M') + ' ' + colored(cur_dir_name, 'blue'))
                else:
                    print('{:<10}'.format(cur_dir.stat().st_size) + ' ' + date.strftime('%Y %b %d %H:%M') + ' ' + cur_dir_name)
        else:
            print('ls: invalid option -- \'' + input_list[1] + '\'')
    else:
        print('ls: too many arguments')
    return

input_string = ''

while True:
    print(colored(pwd_str(), 'blue') + '>', end='')
    input_string = input()
    input_list = list(input_string.split())
    input_list = custom_split(input_list)
    if len(input_list) > 0:
        if input_list[0] == 'exit':
            exit(0, 0)
            break
        if input_list[0] == 'pwd':
            pwd()
        elif input_list[0] == 'cd':
            cd(input_list)
        elif input_list[0] == 'ls':
            ls(input_list)
        elif input_list[0] == 'cat':
            cat(input_list)
        else:
            print(input_string + ': command not found')