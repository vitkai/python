"""
Descr: time management records processing for QTimeRec software
@author: vitkai
Created: Sun May 20 2018 08:15
"""

import __main__ as main
import logging
import pandas as pd
import ruamel.yaml as yml
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


def load_cfg():
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yaml"
    with open(full_path + "/" + yaml_name, 'r') as yaml_file:
    # with open(full_path + "/time_rec_proc.yaml", 'r') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    logger.debug("config in {0}:\n{1}".format(yaml_name, cfg))
    inp_dir = cfg['dirs']['inp_dir']
    outp_dir = cfg['dirs']['outp_dir']

    if inp_dir == "":
        inp_dir = full_path

    if not path.isabs(outp_dir):
        outp_dir = full_path + "/" + outp_dir

    logger.debug("Dirs: Input: {0} || Output: {1}".format(inp_dir, outp_dir))


def imp_df():
    """importing pandas dataframe from csv file"""
    pass

logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

load_cfg()

imp_df()

# some cool stuff to be added here here

logger.debug("That's all folks")
print("That's all folks")
