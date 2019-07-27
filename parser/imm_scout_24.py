"""
Descr: various calculations on loans
@author: vitkai
Created: Sat Jul 27 2017 16:04
"""
import __main__ as main
import logging
import codecs
import matplotlib.pyplot as plt
import pandas as pd
import ruamel.yaml as yml
from os import path  # , listdir, remove, makedirs
#from pprint import pprint  # ,pformat


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

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-' * 10 + '=' * 10 + '-' * 10 + "\n"))

    return logger


def process_fl(inp_data):
    fl_name = path.splitext(filename)[0] + "_tmp.txt"
    with open(fl_name) as file:
        file_contents = file.read()
    
    sub1 = inp_data['boundaries']['list1'][0]
    sub2 = inp_data['boundaries']['list1'][1]
    parse_result = file_contents[file_contents.index(sub1) : file_contents.index(sub2)]
    
    sub1 = inp_data['boundaries']['list2'][0]
    sub2 = inp_data['boundaries']['list2'][1]
    parse_result += file_contents[file_contents.index(sub1) : file_contents.index(sub2)]
    
    #replace new lines with ', '
    parse_result = parse_result.replace('\n', ', ')
    # subst samples with empty string
    for subs in inp_data['to_remove']:
        parse_result = parse_result.replace(subs, '')
        
    for subs, repl in inp_data['replacements'].items():
        parse_result = parse_result.replace(subs, repl)
        
    print(parse_result)

def load_cfg():
    """Loads configuration file and initializes variables"""
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yml"
    #with codecs.open(full_path + "/" + yaml_name, 'r', encoding='utf-8') as yaml_file:
    with codecs.open(full_path + yaml_name, 'r', encoding='utf-8') as yaml_file:
        # with open(full_path + "/time_rec_proc.yaml", 'r') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    #logger.debug("config in {0}:\n{1}".format(yaml_name, cfg))

    return cfg


# main starts here
logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

src_data = load_cfg()

# pprint(pva_calc(30000, 14.5, 1))
# plain_counts(src_data)

process_fl(src_data)

logger.debug("That's all folks")
print("\nThat's all folks")
