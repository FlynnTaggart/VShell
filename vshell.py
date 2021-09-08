import zipfile
import sys
import signal
import os
import shutil
import platform
import io
from datetime import datetime
from termcolor import colored

catting_flag = False

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


# Does not split string by ' ' if the ' ' symbol is in quoted part
def custom_split(input_string):
    splitted = []
    temp_str = ''
    quote_flag = False
    for i in range(len(input_string)):
        if input_string[i] == '\'' and quote_flag == False:
            quote_flag = True
        elif input_string[i] == '\'' and quote_flag == True:
            quote_flag = False
        if i == len(input_string) - 1 or (input_string[i] == ' ' and not quote_flag and not input_string[i + 1] == ' '):
            if i == len(input_string) - 1:
                temp_str += input_string[i]
            splitted.append(temp_str)
            temp_str = ''
        elif input_string[i] == ' ' and not quote_flag:
            continue
        else:
            temp_str += input_string[i]
    return splitted


# Exiting and Ctrl + C handling
def exit(signal, frame):
    global catting_flag
    if catting_flag:
        catting_flag = False
    else:
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
    elif len(input_list) > 2:
        print('ls: too many arguments')
        return
    cur_dir = pwd_str()
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
            cd(['', cur_dir])
            break
        except OSError:
            print('cd: ' + input_list[1] + ': No such file or directory')
            cd(['', cur_dir])
            break
    return


def cat(input_list):
    global  catting_flag
    if len(input_list) == 1:
        catting_flag = True
        while True:
            if not catting_flag:
                break
            else:
                try:
                    print(input())
                except Exception:
                    pass
    elif len(input_list) == 2:
        try:
            cur_dir = pwd_str()
            file_dir_list = input_list[1].split('/')
            if len(file_dir_list) > 1:
                for i in range(len(file_dir_list) - 1):
                    if file_dir_list[i] == '' and i == 0:
                        os.chdir(vshell_root_dir + '/temporary_files')
                        continue
                    elif file_dir_list[i] == '':
                        continue
                    elif file_dir_list[i] == '..' and pwd_str() == '/':
                        continue
            file_name = file_dir_list[len(file_dir_list) - 1]
            if file_name[0] == '\'':
                file_name = file_name[1:-1]
            file = io.open(file_name, 'r', encoding='utf-8')
            cd(['', cur_dir])
            for line in file.readlines():
                print(line, end='')
        except OSError:
            print('cd: ' + input_list[1] + ': No such file')
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

print(colored('Hello!\nType \'exit\' to exit.', 'yellow'))

while True:
    print(colored(pwd_str(), 'blue') + '>', end='')
    input_string = input()
    input_list = custom_split(input_string)
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