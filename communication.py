import shelve
import shutil
import os

import paths


def remove_old():
    shutil.rmtree(paths.COMMUNICATION_DIR)

def prepare():
    if not os.path.exists(paths.COMMUNICATION_DIR):
        os.mkdir(paths.COMMUNICATION_DIR)

def msg_send(msg_type, msg):
    file = shelve.open(paths.COMMUNICATION_FILE)
    file[msg_type] = msg

def msg_read(msg_type):
    file = shelve.open(paths.COMMUNICATION_FILE)
    return file[msg_type]