import logging
import logging.handlers
import hashlib

from datetime import datetime

import constants as C

def logger(filename, file_location=C.TMP_FOLDER, log_filename=None):
    '''
    return logger with handler functionality
    '''
    log_filename = log_filename or "lightform.log"
    # create logger
    my_logger = logging.getLogger(filename)
    my_logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(funcName)s() - %(filename)s:%(lineno)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # Add the log message handler to the logger
    handler = logging.FileHandler(file_location+log_filename)
    handler.setFormatter(formatter)
    if len(my_logger.handlers) > 0:
        return my_logger
    my_logger.addHandler(ch)
    my_logger.addHandler(handler)
    return my_logger


def get_unique_id():
    date = str(datetime.utcnow())
    salt = date
    hash_object = hashlib.md5(salt.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig