from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, Qt
from PySide6 import QtGui, QtWidgets

import threading
import time
import os
import math

import paths
import interactions
import communication
import database


update_interval = 5 # in seconds

process_list = []
ignored_processes = []
logged_processes = []

# Button events
def on_button_remove_from_games_clicked():
    print('xd')

def on_button_add_to_games_clicked():
    global list_other_processes
    selected_other_process = list_other_processes.currentItem()
    list_other_processes.takeItem(list_other_processes.currentRow())
    interactions.add_to_loglist(selected_other_process.text())
    ui_lists_init()

def on_button_add_to_ignorelist_clicked():
    global list_other_processes
    selected_other_process = list_other_processes.currentItem()
    interactions.add_to_ignorelist(selected_other_process.text())
    list_other_processes.takeItem(list_other_processes.currentRow())
    ui_lists_init()

def on_button_remove_from_ignorelist_clicked():
    global list_ignored_processes
    global list_other_processes
    
    selected_ignored_process = list_ignored_processes.currentItem()
    interactions.remove_from_ignorelist(selected_ignored_process.text())
    
    ui_lists_init()

def on_button_add_all_to_ignorelist_clicked():
    global process_list
    global list_ignored_processes
    
    for process in process_list:
        interactions.add_to_ignorelist(process)
    
    ui_lists_init()


def listen_to_pipe():
    global table_games, list_other_processes, list_ignored_processes
    global process_list
    
    try:
        process_list = communication.msg_read('process_list')
    except KeyError as ex:
        list_other_processes.addItem('Is the daemon running?')
    
    print('Listening to shelve')
    
    while True:
        try:
            process_list = communication.msg_read('process_list')
            
            # Logged processes on top!
            logged_games_rows = []
            for logged in logged_processes:
                # logged is the string name of the process
                logged_playtime = database.get_value_where('name', f'\'{logged}\'', 'playtime')
                logged_start_date = database.get_value_where('name', f'\'{logged}\'', 'created_at')
                
                logged_playtime_hours = math.ceil(logged_playtime / 60 / 60)
                logged_playtime_hours_string = f'{logged_playtime_hours} Hour'
                
                if logged_playtime_hours != 1:
                    logged_playtime_hours_string += 's' # plural
                
                logged_games_rows.append(
                    (logged, logged_playtime_hours_string, logged_start_date)
                )
            
            ui_table_set_rows(table_games, logged_games_rows)
            
            # Ignored processes should be ignored COMPLETELY, like the name implies
            # Games that are already flagged for logging, also don't need to be visible in other processes
            for ignored in ignored_processes + logged_processes:
                if ignored in process_list:
                    process_list.remove(ignored)

            ui_list_set_items(list_other_processes, process_list)
        except Exception as ex:
            print(f'Exception occured in listener: {ex}')
        
        time.sleep(update_interval)


def ui_lists_init():
    global list_other_processes, list_ignored_processes, table_games
    global ignored_processes, logged_processes
    
    ignored_processes = interactions.ignorelist_read()
    logged_processes = interactions.loglist_read()
    ui_list_set_items(list_ignored_processes, ignored_processes)

def ui_table_set_rows(table, rows):
    scroll_amount = table.verticalScrollBar().value()
    
    selected_item_text = None
    if table.currentItem() != None:
        selected_item_text = table.currentItem().text()
    
    table.setRowCount(0)
    for row in rows:
        ui_table_insert_row(table, row)
    
    if selected_item_text != None:
        # Check to see if the previously selected item still exists and select it again if possible
        previous_item = table.findItems(selected_item_text, Qt.MatchFlag.MatchContains)
        if len(previous_item) > 0:
            previous_item = previous_item[0]
            
            time.sleep(0.001) # setCurrentItem doesn't seem to work reliably without a little delay (?)
            table.setCurrentItem(previous_item)
    
    table.verticalScrollBar().setValue(scroll_amount)

def ui_table_insert_row(table, row):
    
    
    position = table.rowCount()
    table.insertRow(position)
    
    i = 0
    for _ in row:
        table.setItem(position, i, QtWidgets.QTableWidgetItem(row[i]))
        i += 1

def ui_list_set_items(q_list_widget, items):
    scroll_amount = q_list_widget.verticalScrollBar().value()
    
    selected_item_text = None
    if q_list_widget.currentItem() != None:
        selected_item_text = q_list_widget.currentItem().text()
    
    q_list_widget.clear()
    q_list_widget.addItems(items)
    
    if selected_item_text != None:
        # Check to see if the previously selected item still exists and select it again if possible
        previous_item = q_list_widget.findItems(selected_item_text, Qt.MatchFlag.MatchContains)
        if len(previous_item) > 0:
            previous_item = previous_item[0]
            
            time.sleep(0.001) # setCurrentItem doesn't seem to work reliably without a little delay (?)
            q_list_widget.setCurrentItem(previous_item)
    
    q_list_widget.verticalScrollBar().setValue(scroll_amount)


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

    # Button Presses
    button_remove_from_games.clicked.connect(on_button_remove_from_games_clicked)
    button_add_to_games.clicked.connect(on_button_add_to_games_clicked)
    button_add_to_ignorelist.clicked.connect(on_button_add_to_ignorelist_clicked)
    button_add_all_to_ignorelist.clicked.connect(on_button_add_all_to_ignorelist_clicked)
    button_remove_from_ignorelist.clicked.connect(on_button_remove_from_ignorelist_clicked)
    
    # Init tables and lists
    ui_lists_init()
    
    # Start listening for any changes
    listener_thread = threading.Thread(target=listen_to_pipe, daemon=True)
    listener_thread.start()
    
    app.processEvents()
    app.exec()