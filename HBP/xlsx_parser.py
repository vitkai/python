"""
Descr: module to parse .xlsx file and populate db
@author: vitkai
Created: Wed Feb 19 2019 18:10 MSK
"""
import __main__
import logging
import pandas as pd
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


def import_xlsx(src_fl='my_buh.xlsx'):
    src_fl = full_path + '\\' + src_fl
    work_fl = full_path + '\\' + 'tmp.csv'
    copy2(src_fl, work_fl)
    
    pd_imp = pd.ExcelFile(work_fl).parse()
    
    print(pd_imp.head(5))
    
    return pd_imp

# main starts here
def main():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    
    import_xlsx()
 
    logger.debug("That's all folks")
    print("\nThat's all folks")

if __name__ == "__main__":
    main()
    
# TODO: 
