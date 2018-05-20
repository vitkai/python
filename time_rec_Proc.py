"""
Descr: time management records processing for QTimeRec software
@author: vitkai
Created: Sun May 20 2018 08:15
"""

import __main__ as main
import logging
#import pandas as pd
#import yaml as yml
#from functools import reduce
from os import path#, listdir, remove, makedirs
#from shutil import copy2

def logging_setup():
    logger = logging.getLogger(__name__)
    filename = path.splitext(main.__file__)[0] + '.log'
    handler = logging.FileHandler(filename)

    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    logger.debug("[Debug] Logging was setup")

    return logger

logger = logging_setup()

#some cool stuff here

logger.debug("That's all folks")
print("That's all folks")
