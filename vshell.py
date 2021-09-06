import zipfile
import sys
from termcolor import colored

input_path = sys.argv[1]

archive = zipfile.ZipFile(input_path)
path = zipfile.Path(archive, at='')

def make_date_string(date_tuple):
    date_string = ('{:4}'.format(date_tuple[0]) + ' '
                            + '{:2}'.format(date_tuple[1]) + ' '
                            + '{:2}'.format(date_tuple[2]) + ' '
                            + '{:2}'.format(date_tuple[3]) + ':'
                            + '{:2}'.format(date_tuple[4]) + ':'
                            + '{:2}'.format(date_tuple[5]))
    return date_string

def pwd():
    print('/' + path.name)
    return

def cd(input_list):

    return

def cat(input_list):

    return

def ls(input_list):
    if len(input_list) == 1:
        for filename in archive.namelist():
            temp_name = filename.split('/')
            path_length = len(path.name.split('/'))
            if len(path.name) == 0:
                path_length -= 1
            if temp_name[len(temp_name) - 1] == '':
                if filename.startswith(path.name) and len(temp_name) == path_length + 2:
                    print(colored(temp_name[len(temp_name) - 2], 'blue'))
            else:
                if filename.startswith(path.name) and len(temp_name) == path_length + 1:
                    print(temp_name[len(temp_name) - 1])
    elif len(input_list) == 2:
        if input_list[1] == '-l':
            namelist = archive.namelist()
            infolist = archive.infolist()
            for i in range(len(namelist)):
                temp_name = namelist[i].split('/')
                path_length = len(path.name.split('/'))
                if len(path.name) == 0:
                    path_length -= 1
                if temp_name[len(temp_name) - 1] == '':
                    if namelist[i].startswith(path.name) and len(temp_name) == path_length + 2:
                        print('           ' + make_date_string(infolist[i].date_time) + ' ' + colored(temp_name[len(temp_name) - 2], 'blue'))
                else:
                    if namelist[i].startswith(path.name) and len(temp_name) == path_length + 1:
                        print('{:<10}'.format(infolist[i].file_size) + ' ' + make_date_string(infolist[i].date_time) + ' ' + temp_name[len(temp_name) - 1])
        else:
            print('ls: invalid option -- \'' +  input_list[1] + '\'')
    else:
        print('ls: too many arguments')
    return

input_string = ''

while True:
    print(colored('/' + path.name, 'blue') + '>', end='')
    input_string = input()
    input_list = list(input_string.split())
    if len(input_list) > 0:
        if input_list[0] == 'exit':
            print(colored('Exiting VShell...', 'green'))
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