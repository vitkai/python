"""
Descr: module to parse .xlsx file and populate db
@author: vitkai
Created: Wed Feb 19 2019 18:10 MSK
"""
import __main__
# import codecs
# import locale
import logging
import pandas as pd
# import sys
import yaml as yml
from os import path
from shutil import copy2
# import sqlite3
# from sqlite3 import Error
# from time import gmtime, strftime

def logging_setup():
    logger = logging.getLogger(__name__)
    filename = path.splitext(__main__.__file__)[0] + '.log'
    handler = logging.FileHandler(filename)

    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-' * 10 + '=' * 10 + '-' * 10 + "\n"))

    return logger


def load_cfg():
    # read configuration
    cfg_file = full_path + '\\' + "xlsx_parser.yaml" 
    msg = 'Loading configuration:\nOpening {}'.format(cfg_file)
    logger.debug(msg)
    print(msg)
    with open(cfg_file, 'r') as yml_fl:
        cfg = yml.safe_load(yml_fl)
    
    msg = 'Config loaded successfully'
    logger.debug(msg)
    print(msg)
    
    print(cfg)
    return cfg
    

def check_cfg(cfg):
    # configuration check
    
    for cat in cfg['categories']:
        if cat in cfg[2020]['spent']:
            print('{} | {} '.format(cat, cfg[2020]['spent'][cat]['val']))


def import_xlsx(src_fl='my_buh.xlsx'):
    
    src_fl = full_path + '\\' + src_fl
    work_fl = full_path + '\\' + 'tmp.csv'
    copy2(src_fl, work_fl)
    
    pd_imp = pd.ExcelFile(work_fl).parse()
    # pd_imp = pd.read_excel(work_fl, encoding='utf-8')
    
    # sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
    # locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
    
    tmp = pd_imp.head(5) #.to_html()
    print(tmp) # .encode('utf-8'))

    return pd_imp
    

# main starts here
def main():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    
    # import_xlsx()
    conf = load_cfg()
    check_cfg(conf)
 
    logger.debug("That's all folks")
    print("\nThat's all folks")

if __name__ == "__main__":
    main()
    
# TODO: 
