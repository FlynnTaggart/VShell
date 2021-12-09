import io
import os
import sys
import zipfile
from termcolor import colored


class Archive:
    vshell_root_dir = ''
    user_os = ''
    catting_flag = False

    def __init__(self, input_path: str, user_os: str):
        self.input_path = input_path
        self.user_os = user_os
        try:
            self.archive = zipfile.ZipFile(input_path)
            self.path = zipfile.Path(self.archive, at='')
        except Exception:
            print(colored('\nNo such file or directory', 'red'))
            sys.exit(0)
        self.vshell_root_dir = os.getcwd()
        if user_os == 'Windows':
            self.vshell_root_dir = self.vshell_root_dir.replace('\\', '/')

    def pwd(self):
        print('/' + '/'.join(str(self.path).split('/')[2:]))
        return

    def pwd_str(self):
        return '/' + '/'.join(str(self.path).split('/')[2:])

    def cd(self, input_list: list):
        if len(input_list) == 1:
            return
        elif len(input_list) > 2:
            print('ls: too many arguments')
            return
        cur_path = self.path
        change_dir_list = input_list[1].split('/')
        for i in range(len(change_dir_list)):
            if change_dir_list[i] == '' and i == 0:
                self.path = zipfile.Path(self.archive, at='')
                continue
            elif change_dir_list[i] == '':
                continue
            elif change_dir_list[i] == '..' and self.pwd_str() == '/':
                continue
            elif change_dir_list[i] == '.':
                continue
            elif change_dir_list[i] == '..':
                self.path = zipfile.Path(self.archive, at='/'.join(self.pwd_str()[1:-1].split('/')[:-1]))
                continue
            if not (change_dir_list[i] in self.ls_str([''])):
                print('cd: ' + input_list[1] + ': No such file or directory')
                self.path = cur_path
                break
            self.path = self.path / change_dir_list[i]
            if not self.path.is_dir():
                print('cd: ' + input_list[1] + ': Not a directory')
                self.path = cur_path
                break
        if str(self.path)[len(str(self.path)) - 1] != '/':
            self.path = zipfile.Path(self.archive, at=self.pwd_str()[1:] + '/')
        return

    def cat(self, input_list: list):
        if len(input_list) == 1:
            self.catting_flag = True
            while True:
                if not self.catting_flag:
                    break
                else:
                    try:
                        print(input())
                    except Exception:
                        pass
            return
        elif len(input_list) > 2:
            print('cat: too many arguments')
            return
        cur_path = self.path
        file_dir_list = input_list[1].split('/')
        if len(file_dir_list) > 1:
            for i in range(len(file_dir_list) - 1):
                if file_dir_list[i] == '' and i == 0:
                    self.path = zipfile.Path(self.archive, at='')
                    continue
                elif file_dir_list[i] == '':
                    continue
                elif file_dir_list[i] == '..' and self.pwd_str() == '/':
                    continue
                elif file_dir_list[i] == '.':
                    continue
                elif file_dir_list[i] == '..':
                    self.path = zipfile.Path(self.archive, at='/'.join(self.pwd_str()[1:-1].split('/')[:-1]))
                    continue
                if not (file_dir_list[i] in self.ls_str([''])):
                    print('cat: ' + input_list[1] + ': No such file')
                    self.path = cur_path
                    return
                self.path = self.path / file_dir_list[i]
                if not self.path.is_dir():
                    print('cat: ' + input_list[1] + ': No such file')
                    self.path = cur_path
                    return
        file_name = file_dir_list[len(file_dir_list) - 1]
        if file_name[0] == '\'':
            file_name = file_name[1:-1]
        self.path = self.path / file_name
        if (not self.path.exists()) or (self.path.is_dir()):
            print('cat: ' + input_list[1] + ': No such file')
            self.path = cur_path
            return
        try:
            self.archive = zipfile.ZipFile(self.input_path)
            with self.archive as archive:
                with archive.open(self.pwd_str()[1:]) as file:
                    print(file.read().decode())
        except UnicodeDecodeError:
            self.archive = zipfile.ZipFile(self.input_path)
            with self.archive as archive:
                with archive.open(self.pwd_str()[1:]) as file:
                    for line in file.readlines():
                        print(line, end='')
                    print()
        except Exception:
            print('cat: ' + input_list[1] + ': No such file')
            self.path = cur_path
            return
        self.path = cur_path
        return

    def ls_str(self, input_list: str):
        ls_res = ""
        if len(input_list) == 1:
            for filename in self.archive.namelist():
                temp_name = filename.split('/')
                path_length = len(self.pwd_str()[1:-1].split('/'))
                if len(self.pwd_str()[1:-1]) == 0:
                    path_length -= 1
                if temp_name[len(temp_name) - 1] == '':
                    if filename.startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 2:
                        ls_res += temp_name[len(temp_name) - 2] + '\n'
                else:
                    if filename.startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 1:
                        ls_res += temp_name[len(temp_name) - 1] + '\n'
        return ls_res

    def ls(self, input_list: str):
        if len(input_list) == 1:
            for filename in self.archive.namelist():
                temp_name = filename.split('/')
                path_length = len(self.pwd_str()[1:-1].split('/'))
                if len(self.pwd_str()[1:-1]) == 0:
                    path_length -= 1
                if temp_name[len(temp_name) - 1] == '':
                    if filename.startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 2:
                        print(colored(temp_name[len(temp_name) - 2], 'blue'))
                else:
                    if filename.startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 1:
                        print(temp_name[len(temp_name) - 1])
        elif len(input_list) == 2:
            if input_list[1] == '-l':
                namelist = self.archive.namelist()
                infolist = self.archive.infolist()
                for i in range(len(namelist)):
                    temp_name = namelist[i].split('/')
                    path_length = len(self.pwd_str()[1:-1].split('/'))
                    if len(self.pwd_str()[1:-1]) == 0:
                        path_length -= 1
                    if temp_name[len(temp_name) - 1] == '':
                        if namelist[i].startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 2:
                            print('           ' + self.make_date_string(infolist[i].date_time) + ' ' + colored(
                                temp_name[len(temp_name) - 2], 'blue'))
                    else:
                        if namelist[i].startswith(self.pwd_str()[1:-1]) and len(temp_name) == path_length + 1:
                            print('{:<10}'.format(infolist[i].file_size) + ' ' + self.make_date_string(
                                infolist[i].date_time) + ' ' + temp_name[len(temp_name) - 1])
            else:
                print('ls: invalid option -- \'' + input_list[1] + '\'')
        else:
            print('ls: too many arguments')
        return

    def help(self):
        try:
            help_file = io.open(self.vshell_root_dir + '/help.txt', 'r', encoding='utf-8')
            for line in help_file.readlines():
                print(line, end='')
            print('')
            help_file.close()
        except OSError:
            print('Welcome to VShell!')

    @staticmethod
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
            if i == len(input_string) - 1 or (
                    input_string[i] == ' ' and not quote_flag and not input_string[i + 1] == ' '):
                if i == len(input_string) - 1:
                    temp_str += input_string[i]
                splitted.append(temp_str)
                temp_str = ''
            elif input_string[i] == ' ' and not quote_flag:
                continue
            else:
                temp_str += input_string[i]
        return splitted

    @staticmethod
    def make_date_string(date_tuple):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        date_string = ('{:04d}'.format(date_tuple[0]) + ' '
                       + months[int('{:02d}'.format(date_tuple[1])) - 1] + ' '
                       + '{:02d}'.format(date_tuple[2]) + ' '
                       + '{:02d}'.format(date_tuple[3]) + ':'
                       + '{:02d}'.format(date_tuple[4]) + ':'
                       + '{:02d}'.format(date_tuple[5]))
        return date_string
