# This script should be hooked into some kind of UI (here: gui.py)
import paths
import os

console_prefix = '[interactions.py]'


def _file_writeline(file_path, line):
    loglist = open(file_path, 'a+')
    if not line in loglist.readlines():
        loglist.writelines(f'{line}\n')
    loglist.close()

def _file_removeline(file_path, line_to_remove):
    file = open(file_path, 'r')
    
    new_lines = []
    
    for line in file.readlines():
        line = line.rstrip()
        if line != line_to_remove:
            new_lines.append(f'{line}\n')
    
    file.close()
    
    file = open(file_path, 'w') # overwrite
    file.writelines(new_lines)
    file.close()


def add_to_loglist(process_name):
    _file_writeline(paths.LOGLIST, process_name)

def add_to_ignorelist(process_name):
    _file_writeline(paths.IGNORELIST, process_name)

def remove_from_loglist(process_name):
    _file_removeline(paths.LOGLIST, process_name)

def remove_from_ignorelist(process_name):
    _file_removeline(paths.IGNORELIST, process_name)

def ignorelist_read():
    ignored_processes = []
    
    if os.path.exists(paths.IGNORELIST):
        ignorelist = open(paths.IGNORELIST, 'r')
        for line in ignorelist.readlines():
            line_sanitized = line.replace('\n', '')
            ignored_processes.append(line_sanitized)
            
        ignorelist.close()
    
    return ignored_processes