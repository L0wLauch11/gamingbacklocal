import os, inspect

_current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

SAVEDATA_DIR =  './savedata'
GAMELOG = SAVEDATA_DIR + '/game_log.sqlite'

# These processes will be completely ignored
IGNORELIST = SAVEDATA_DIR + '/ignorelist.txt'

# These processes are explicitly made important by the user, the UI should communicate this
LOGLIST = SAVEDATA_DIR + '/loglist.txt'

MAIN_WINDOW = './qt/mainwindow.ui'

COMMUNICATION_DIR = './shelve'
COMMUNICATION_FILE = f'{COMMUNICATION_DIR}/comm_localbacklog.shelve'