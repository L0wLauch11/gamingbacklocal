from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile

import paths
import interactions


def on_button_remove_from_games_clicked():
    print('xd')

def on_button_add_to_games_clicked():
    print('xd1')

def on_button_add_to_ignorelist_clicked():
    print('xd12')

def on_button_remove_from_ignorelist_clicked():
    print('xd14')

if __name__ == "__main__":
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
    table_games = window.tableYourGames
    list_other_processes = window.listOtherProcesses
    list_ignored_processes = window.listIgnoredProcesses
    
    button_remove_from_games = window.buttonRemoveFromGames
    button_add_to_games = window.buttonAddToGames
    button_add_to_ignorelist = window.buttonIgnore
    button_remove_from_ignorelist = window.buttonRespect
    
    button_remove_from_games.clicked.connect(on_button_remove_from_games_clicked)
    button_add_to_games.clicked.connect(on_button_add_to_games_clicked)
    button_add_to_ignorelist.clicked.connect(on_button_add_to_ignorelist_clicked)
    button_remove_from_ignorelist.clicked.connect(on_button_remove_from_ignorelist_clicked)
    
    # Init tables and lists
    table_games
    
    
    app.processEvents()
    app.exec()