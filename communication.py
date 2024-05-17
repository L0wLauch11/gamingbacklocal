from enum import Enum
import shelve
import os

import paths


def remove_old():
    if os.path.exists(paths.COMMUNICATION_FILE):
        os.remove(paths.COMMUNICATION_FILE)

def msg_send(msg_type, msg):
    file = shelve.open(paths.COMMUNICATION_FILE)
    file[msg_type] = msg

def msg_read(msg_type):
    file = shelve.open(paths.COMMUNICATION_FILE)
    return file[msg_type]