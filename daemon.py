import psutil
import sqlite3
import time
from datetime import datetime
import atexit

import paths
import communication
import database

console_prefix = '[daemon.py]'
logging_interval = 5 # In Seconds

db_connection = sqlite3.connect(paths.GAMELOG)
db_cursor = db_connection.cursor()
db_table_name = 'games'
db_table = f'{db_table_name}(name TEXT PRIMARY KEY, playtime INTEGER, created_at STRING)'


def watch_processes():
    watched_processes = []
    
    for process in psutil.process_iter(['name']):
        try:
            process_name = process.info['name']
            
            # Even if a program uses multiple processes, we only want to "watch" it once
            if process_name in watched_processes:
                continue
            
            database_write_game(process_name)
            watched_processes.append(process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    communication.msg_send('process_list', watched_processes)
    
    
def database_write_game(game_name):
    # Every 'logging_interval' seconds we get a process list
    # So we know the process has been running for approx. 'logging_interval' seconds
    # That's why we can take 'logging_interval' and assume the game/process has been running for
    # 'logging_interval' seconds, this will of course cause slight deviations if player closes the process inbetween
    # the 'logging_interval' but no matter, it's accurate enough for our playtime logger
    game_session_time = logging_interval
    
    logged_playtime = database.get_value_where('name', f'\'{game_name}\'', 'playtime')
    if logged_playtime == None:
        logged_playtime = 0
        
    game_total_playtime = logged_playtime + game_session_time
    
    logged_created_at = database.get_value_where('name', f'\'{game_name}\'', 'created_at')
    if logged_created_at == None:
        logged_created_at = datetime.now().strftime('%B %d %Y - %H:%M:%S')
    
    database.replace_into(game_name, game_total_playtime, logged_created_at)

    #print(f'{console_prefix} {game_name} total playtime: {game_total_playtime}')

if __name__ == '__main__':
    database.migrate()
    
    communication.prepare()
    atexit.register(communication.remove_old)
    
    while True:
        watch_processes()
        time.sleep(logging_interval)