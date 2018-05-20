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

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('*'*10 + "\n"))

    return logger


def load_cfg():
    """

    :rtype: tuple
    """
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yaml"
    with open(full_path + "/" + yaml_name, 'r') as yaml_file:
    # with open(full_path + "/time_rec_proc.yaml", 'r') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    logger.debug("config in {0}:\n{1}".format(yaml_name, cfg))
    src_dir = cfg['dirs']['inp_dir']
    dst_dir = cfg['dirs']['outp_dir']

    if src_dir == "":
        src_dir = full_path + "/"
    else:
        src_dir += "/"

    if not path.isabs(dst_dir):
        dst_dir = full_path + "/" + dst_dir + "/"

    logger.debug("Dirs: Input: {0} || Output: {1}".format(src_dir, dst_dir))

    return src_dir, dst_dir


def imp_df(src_dir):
    """importing pandas dataframe from csv file"""

    #global full_path
    if not path.isabs(src_dir):
        src_dir = full_path + '/' + src_dir
        logger.debug("Path is relative")
    logger.debug("Input dir is: {0}|| Full path is: {1}".format(src_dir, full_path))
    # TODO 1)replace headings in imported files 2)add columns head into yaml cfg
    df_imported = pd.read_csv(src_dir + "qtimerec_2018_03.csv", encoding='UTF8')

    logger.debug("DF imported from csv:\n{0}".format(df_imported.head()))


# main starts here
logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

inp_dir, outp_dir = load_cfg()

imp_df(inp_dir)

# some cool stuff to be added here here

logger.debug("That's all folks")
print("That's all folks")
