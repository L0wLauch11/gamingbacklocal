from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile

import threading
import time
import os

import paths
import interactions
import communication


update_interval = 5 # in seconds

process_list = []
ignored_processes = []
game_processes = []

selected_other_process = None
selected_ignored_process = None
selected_game_process = None


def on_button_remove_from_games_clicked():
    print('xd')

def on_button_add_to_games_clicked():
    print('xd1')

def on_button_add_to_ignorelist_clicked():
    print('xd12')

def on_button_remove_from_ignorelist_clicked():
    print('xd14')

def on_button_add_all_to_ignorelist_clicked():
    global process_list
    global list_ignored_processes
    
    ignorelist = open(paths.IGNORELIST, 'a+')
    for process in process_list:
        if not process in ignorelist.readlines():
            ignorelist.writelines(process + '\n')
    ignorelist.close()
    
    ignored_processes = interactions.ignorelist_read()
    
    list_ignored_processes.clear()
    list_ignored_processes.addItems(ignored_processes)


def listen_to_pipe():
    global table_games, list_other_processes, list_ignored_processes
    global process_list
    
    try:
        current_running_processes = communication.msg_read('process_list')
    except KeyError as ex:
        list_other_processes.addItem('Is the daemon running?')
    
    print('Listening to shelve')

    while True:
        try:
            current_running_processes = communication.msg_read('process_list')
            
            # Ignored processes should be ignored COMPLETELY, like the name implies
            for ignored in ignored_processes:
                #print(current_running_processes)2
                if ignored in current_running_processes:
                    current_running_processes.remove(ignored)
            
            if len(process_list) != len(current_running_processes):
                list_other_processes.clear()
                list_other_processes.addItems(process_list)

                # Should be registered at the end to not have duplicate entries
                process_list = current_running_processes
        except Exception as ex:
            print(f'Exception occured in listener: {ex}')
        
        time.sleep(update_interval)

if __name__ == '__main__':
    communication.prepare()
    
    ui_file = QFile(paths.MAIN_WINDOW)
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    
    # app needs to be initialized after loader
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    window = loader.load(ui_file, None)
    window.show()
    
    # Breakout important UI elements
    global table_games, list_other_processes, list_ignored_processes
    table_games = window.tableYourGames
    list_other_processes = window.listOtherProcesses
    list_ignored_processes = window.listIgnoredProcesses
    
    button_remove_from_games = window.buttonRemoveFromGames
    button_add_to_games = window.buttonAddToGames
    button_add_to_ignorelist = window.buttonIgnore
    button_add_all_to_ignorelist = window.buttonIgnoreAll
    button_remove_from_ignorelist = window.buttonRespect
    
    button_remove_from_games.clicked.connect(on_button_remove_from_games_clicked)
    button_add_to_games.clicked.connect(on_button_add_to_games_clicked)
    button_add_to_ignorelist.clicked.connect(on_button_add_to_ignorelist_clicked)
    button_add_all_to_ignorelist.clicked.connect(on_button_add_all_to_ignorelist_clicked)
    button_remove_from_ignorelist.clicked.connect(on_button_remove_from_ignorelist_clicked)
    
    # Init tables and lists
    ignored_processes = interactions.ignorelist_read()
    
    list_ignored_processes.addItems(ignored_processes)
    
    # Start listening for any changes
    listener_thread = threading.Thread(target=listen_to_pipe, daemon=True)
    listener_thread.start()
    
    app.processEvents()
    app.exec()