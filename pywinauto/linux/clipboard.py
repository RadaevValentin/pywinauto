# Copyright (c) 2016 Ivan Magazinnik
import subprocess
import sys


def cmd_exists(cmd):
    """Check is app exist"""
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def set_up_clipboard(is_input):
    """Find clipboard app in system"""
    command = []
    if sys.platform == 'linux' or sys.platform == 'linux2':
        if cmd_exists('xclip'):
            command.append('xclip')
            if is_input:
                command.append('-selection')
                command.append('c')
            else:
                command.append('-selection')
                command.append('c')
                command.append('-o')
        elif cmd_exists('xsel'):
            command.append('xsel')
            command.append('-b')
            if is_input:
                command.append('-i')
            else:
                command.append('-o')
    elif sys.platform == 'darwin':
        if is_input:
            command.append('pbcopy')
            command.append('w')
        else:
            command.append('pbpaste')
            command.append('r')
    if not command:
        raise NameError('No clipboard manager')
    return command


def get_data():
    """Get data from clipboard"""
    command = set_up_clipboard(is_input=False)
    process = subprocess.Popen(command,stdout=subprocess.PIPE, close_fds=True)
    stdout = process.communicate()
    return stdout[0].decode('utf-8')


def set_data(text):
    """Put some text to clipboard"""
    command = set_up_clipboard(is_input=True)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, close_fds=True)
    process.communicate(input=text.encode('utf-8'))
