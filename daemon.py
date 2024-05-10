import asyncio
import websockets
import json
import time
import os
import inspect
import subprocess
import sqlite3

console_prefix = '[daemon.py]'


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

nodejs = current_dir + '/external/node/node.exe'
arrpc = current_dir + '/external/arrpc/src'


# SQLite DB Shit
savedata_dir = current_dir + '/savedata'
gamelog_path = savedata_dir + '/game_log.sqlite'

db_connection = sqlite3.connect(gamelog_path)
db_cursor = db_connection.cursor()
db_table_name = 'games'
db_table = f'{db_table_name}(app_id INTEGER PRIMARY KEY, name TEXT, playtime INTEGER)'


running_games = {}


async def handle_websocket(uri):
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                
                # This means a game is played (or stopped being played)!
                on_message_receive(message)
    except Exception as ex:
        # Could be that the python script tries its schenanigans before
        # arRPC is initialized -> hence this try, catch
        print(ex)
        print("Connection failed... trying again")
        handle_websocket()


def on_message_receive(message):
    data = json.loads(message)
    
    if data['activity']:
        game = data['activity']
        
        # Only set once; arRPC sends the same game more than once, probably for packet loss reasons
        if not data['pid'] in running_games:
            running_games[data['pid']] = {
                'name': game['name'],
                'app_id': game['application_id'],
                'started_timestamp': int(time.time()) # casting int reduces the timestamp to seconds
            }
        
    # Game has been stopped
    elif data['activity'] == None and data['pid'] != None:
        current_game = running_games[data['pid']]
        if current_game:
            time_diff = int(time.time()) - current_game['started_timestamp']
            current_game['session_time'] = time_diff
            game_name = current_game['name']
            
            print(f'{console_prefix} {game_name} ran for {str(time_diff)}s')
            database_write_game(current_game)
            
            del running_games[data['pid']]
    
    #print(running_games)


def database_migrate():
    global db_cursor
    db_cursor.execute(f'CREATE TABLE IF NOT EXISTS {db_table}')
    
def database_write_game(running_game):
    # I hate SQL with a passion
    # running_game: name, app_id, started_timestamp, session_time
    global db_cursor
    global db_connection
    
    game_app_id = running_game['app_id']
    game_name = running_game['name']
    game_session_time = running_game['session_time']
    
    logged_playtime = db_cursor.execute(f'SELECT playtime FROM {db_table_name} WHERE app_id={game_app_id}').fetchone()
    if logged_playtime == None:
        logged_playtime = 0
    else:
        logged_playtime = logged_playtime[0] # db returns touple
    
    print(game_session_time)
    game_total_playtime = logged_playtime + game_session_time
    
    db_cursor.execute(f'REPLACE INTO {db_table_name} VALUES({game_app_id}, \'{game_name}\', {game_total_playtime})')
    db_connection.commit()


async def main():
    uri = "ws://localhost:1337"
    await handle_websocket(uri)

if __name__ == '__main__':
    # Init DB should be done first
    database_migrate()
    
    # Get arRPC ready
    subprocess.Popen([nodejs, arrpc])
    
    # Connect to socket
    asyncio.run(main())