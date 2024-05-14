import os, inspect

_current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

SAVEDATA_DIR = _current_dir + '/savedata'
GAMELOG = SAVEDATA_DIR + '/game_log.sqlite'

# These processes will be completely ignored
IGNORELIST = SAVEDATA_DIR + '/ignorelist.txt'

# These processes are explicitly made important by the user, the UI should communicate this
LOGLIST = SAVEDATA_DIR + '/loglist.txt'


MAIN_WINDOW = _current_dir + '/qt/mainwindow.ui'