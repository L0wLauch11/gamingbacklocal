import sqlite3
import paths

db_connection = sqlite3.connect(paths.GAMELOG)
db_cursor = db_connection.cursor()
db_table_name = 'games'
db_table = f'{db_table_name}(name TEXT PRIMARY KEY, playtime INTEGER, created_at STRING)'

def migrate():
    global db_cursor
    db_cursor.execute(f'CREATE TABLE IF NOT EXISTS {db_table}')

def get_value_where(key, key_value, value):
    retval = db_cursor.execute(
        f'SELECT {value} FROM {db_table_name} WHERE {key}={key_value}'
    ).fetchone()
    
    if retval != None:
        retval = retval[0] # fetchone() always returns tuple
    
    return retval

def replace_into(name, playtime, created_at):
    db_cursor.execute(f'REPLACE INTO {db_table_name} VALUES(\'{name}\', \'{playtime}\', \'{created_at}\')')
    db_connection.commit()