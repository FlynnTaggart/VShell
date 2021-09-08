import io
import os
import shutil
import zipfile
from termcolor import colored
from datetime import datetime


class Archive:
    vshell_root_dir = ''
    user_os = ''
    catting_flag = False

    def __init__(self, input_path: str, user_os: str):
        self.user_os = user_os
        zip_file = zipfile.ZipFile(input_path)
        vshell_root_dir = os.getcwd()
        if user_os == 'Windows':
            self.vshell_root_dir = vshell_root_dir.replace('\\', '/')

        try:
            os.mkdir('temporary_files')
        except FileExistsError:
            shutil.rmtree('temporary_files')
            os.mkdir('temporary_files')
        os.chdir('temporary_files')

        zip_file.extractall()

    def pwd(self):
        current_dir = os.getcwd()
        if self.user_os == 'Windows':
            current_dir = current_dir.replace('\\', '/')
        print(current_dir[len(self.vshell_root_dir + '/temporary_files'):] + '/')
        return

    def pwd_str(self):
        current_dir = os.getcwd()
        if self.user_os == 'Windows':
            current_dir = current_dir.replace('\\', '/')
        str = current_dir[len(self.vshell_root_dir + '/temporary_files'):] + '/'
        return str

    def cd(self, input_list: list):
        if len(input_list) == 1:
            return
        elif len(input_list) > 2:
            print('ls: too many arguments')
            return
        cur_dir = self.pwd_str()
        change_dir_list = input_list[1].split('/')
        for i in range(len(change_dir_list)):
            if change_dir_list[i] == '' and i == 0:
                os.chdir(self.vshell_root_dir + '/temporary_files')
                continue
            elif change_dir_list[i] == '':
                continue
            elif change_dir_list[i] == '..' and self.pwd_str() == '/':
                continue
            try:
                os.chdir(change_dir_list[i])
            except NotADirectoryError:
                print('cd: ' + input_list[1] + ': Not a directory')
                self.cd(['', cur_dir])
                break
            except OSError:
                print('cd: ' + input_list[1] + ': No such file or directory')
                self.cd(['', cur_dir])
                break
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
        elif len(input_list) == 2:
            try:
                cur_dir = self.pwd_str()
                file_dir_list = input_list[1].split('/')
                if len(file_dir_list) > 1:
                    for i in range(len(file_dir_list) - 1):
                        if file_dir_list[i] == '' and i == 0:
                            os.chdir(self.vshell_root_dir + '/temporary_files')
                            continue
                        elif file_dir_list[i] == '':
                            continue
                        elif file_dir_list[i] == '..' and self.pwd_str() == '/':
                            continue
                file_name = file_dir_list[len(file_dir_list) - 1]
                if file_name[0] == '\'':
                    file_name = file_name[1:-1]
                file = io.open(file_name, 'r', encoding='utf-8')
                self.cd(['', cur_dir])
                for line in file.readlines():
                    print(line, end='')
                file.close()
            except OSError:
                print('cd: ' + input_list[1] + ': No such file')
        return

    def ls(self, input_list: str):
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
                        print('{:<10}'.format(cur_dir.stat().st_size) + ' ' + date.strftime(
                            '%Y %b %d %H:%M') + ' ' + cur_dir_name)
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
