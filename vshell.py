import archive
import sys
import signal
import os
import shutil
import platform
from termcolor import colored


# Exiting and Ctrl + C handling
def exit(signal, frame):
    if archive.catting_flag:
        archive.catting_flag = False
    else:
        os.chdir(archive.vshell_root_dir)
        try:
            shutil.rmtree('temporary_files')
        except Exception:
            pass
        print(colored('\nExiting VShell...', 'green'))
        sys.exit(0)


user_os = platform.system()

try:
    input_path = sys.argv[1]
except Exception:
    print(colored('\nNo such file or directory', 'red'))
    sys.exit(0)

archive = archive.Archive(input_path, user_os)

signal.signal(signal.SIGINT, exit)

input_string = ''

print(colored('Hello!\nType \'help\' for help.', 'yellow'))

while True:
    print(colored(archive.pwd_str(), 'blue') + '>', end='')
    input_string = input()
    input_list = archive.custom_split(input_string)
    if len(input_list) > 0:
        if input_list[0] == 'exit':
            exit(0, 0)
            break
        if input_list[0] == 'pwd':
            archive.pwd()
        elif input_list[0] == 'cd':
            archive.cd(input_list)
        elif input_list[0] == 'ls':
            archive.ls(input_list)
        elif input_list[0] == 'cat':
            archive.cat(input_list)
        elif input_list[0] == 'help':
            archive.help()
        else:
            print(input_string + ': command not found')