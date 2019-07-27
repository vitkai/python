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
    for subs in inp_data['to_remove']:
        parse_result = parse_result.replace(subs, '')
        
    parse_result = parse_result.replace('\n\n', '\n')
    
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

    # process directories
    global inp_dir, outp_dir
    inp_dir = cfg['dirs']['inp_dir']
    outp_dir = cfg['dirs']['outp_dir']

    logger.debug("Dirs: Input: {0} || Output: {1}".format(inp_dir, outp_dir))
    return cfg


def plain_counts(inp_data):
    for yr in inp_data['parameters']['years']['yr_list']:

        debt_remain = inp_data['parameters']['debt_pv']
        pprint(yr)


def calc_pay_off_term(inp_data, double):
    calcs_data_list = []

    ir_month = inp_data['parameters']['interest_rates']['debt_year_ir'] / (100 * 12)  # 0.1445 / 12
    debt_remainder = inp_data['parameters']['debt']['pv']  # 1228484.63
    debt_length = inp_data['parameters']['debt']['term']['periods_total'] - inp_data['parameters']['debt']['term']\
        ['periods_passed']  # 350 - 47
    months_passed: int = 0
    month_annuity = period_annuity_calc(debt_remainder, debt_length, months_passed, ir_month)
    if double:
        month_payment = 0
        debt_pay_off_sum = month_annuity
    else:
        month_payment = inp_data['parameters']['payments']['month_periodic']  # 30000
        if month_payment < month_annuity:
            msg = "Warning: month payment is smaller than annuity!"
            print(msg)
            logger.warning(msg)
        debt_pay_off_sum = month_payment
    # cycle by periods (months)
    while (months_passed < debt_length) and (debt_remainder > debt_pay_off_sum):
        month_interest = debt_remainder * ir_month
        payment_to_debt = month_annuity - month_interest
        debt_remainder = debt_remainder - payment_to_debt
        # if paying double always just use annuity value *2
        if double:
            month_payment = month_annuity * 2
        month_payment_extra = month_payment - month_annuity
        months_passed += 1
        if month_payment_extra > 0:
            debt_remainder = debt_remainder - month_payment_extra
        """print(f"{'-' * 5}month = {months_passed}{'-' * 5}")
        print(f"month_annuity = {month_annuity}")
        print(f"month_interest = {month_interest}")
        print(f"payment_to_debt = {payment_to_debt}")
        print(f"debt_remainder = {debt_remainder}")"""
        # add row into the list of values
        calcs_data_list.append([month_annuity, month_interest, payment_to_debt, debt_remainder])
        # calculate new annuity
        month_annuity = period_annuity_calc(debt_remainder, debt_length, months_passed, ir_month)

    return calcs_data_list, months_passed


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
