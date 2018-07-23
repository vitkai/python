"""
Descr: various calculations on loans
@author: vitkai
Created: Mon Jul 23 2018 20:34
"""
import __main__ as main
import logging
import ruamel.yaml as yml
import codecs
from os import path  # , listdir, remove, makedirs
from pprint import pprint  # ,pformat


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


def load_cfg():
    """Loads configuration file and initializes variables"""
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yaml"
    with codecs.open(full_path + "/" + yaml_name, 'r', encoding='utf-8') as yaml_file:
        # with open(full_path + "/time_rec_proc.yaml", 'r') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    logger.debug("config in {0}:\n{1}".format(yaml_name, cfg))

    # process directories
    global inp_dir, outp_dir
    inp_dir = cfg['dirs']['inp_dir']
    outp_dir = cfg['dirs']['outp_dir']

    if inp_dir == "":
        inp_dir = full_path + "/"
    else:
        inp_dir += "/"

    if not path.isabs(outp_dir):
        outp_dir = full_path + "/" + outp_dir + "/"

    logger.debug("Dirs: Input: {0} || Output: {1}".format(inp_dir, outp_dir))


def pva_calc(per_payment, rate_per_period, periods_quant):
    """http://financeformulas.net/Present_Value_of_Annuity.html"""
    return per_payment * ((1-(1+rate_per_period)**(-periods_quant)) / rate_per_period)


# main starts here
logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

load_cfg()

pprint(pva_calc(30000, 14.5, 1))

logger.debug("That's all folks")
pprint("That's all folks")
