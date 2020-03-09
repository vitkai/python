"""
Descr: various calculations on loans
@author: vitkai
Created: Mon Jul 23 2018 20:34
"""
import __main__ as main
import logging
import codecs
import matplotlib.pyplot as plt
import pandas as pd
#import ruamel.yaml as yml
import yaml as yml
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


def load_cfg():
    """Loads configuration file and initializes variables"""
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yaml"
    with codecs.open(full_path + "/" + yaml_name, 'r', encoding='utf-8') as yaml_file:
    #with codecs.open(full_path + yaml_name, 'r', encoding='utf-8') as yaml_file:
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
    return cfg


def pva_calc(per_payment, rate_per_period, periods_quant):
    """http://financeformulas.net/Present_Value_of_Annuity.html"""
    return per_payment * ((1-(1+rate_per_period)**(-periods_quant)) / rate_per_period)


def period_annuity_calc(debt_amount, debt_period, periods_passed, period_ir):
    if periods_passed > debt_period:
        print("Warning: passed period is bigger than debt period")
        logger.warning("passed period is bigger than debt period")
    return debt_amount * (period_ir + period_ir /((1+period_ir)**(debt_period-periods_passed) - 1))


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

debt_columns = ('Annuity', 'Interest', 'Payed to debt', 'Debt Remainder')
# df_calcs = pd.DataFrame(columns=debt_columns)

all_calcs_dict = {}

concat_df = pd.DataFrame()
for strat in src_data['parameters']['payments']['strategy']:
    # calculate pay off values

    calcs_dict = {}

    double_flag = (strat == 'double')
    data_list, month_quant = calc_pay_off_term(src_data, double_flag)
    print(f"\n{'-=-' * 2}For {strat} strategy:{'-=-' * 2}")
    print(f"{'-=-' * 2}Time total: {month_quant // 12}years {month_quant % 12} months{'-=-' * 2}")


    calcs_dict['Term'] = month_quant
    calcs_dict['Data'] = data_list

    logger.debug(f"Pay off values for {strat}: {debt_columns}\n{data_list[:3]}\n...\n{data_list[-3:]}")

    all_calcs_dict[strat] = calcs_dict

    # df2 = data_list to be converted
#    df_combined = pd.concat([concat_df, df2], axis=1)
#    concat_df = df_combined  # for next concat

    # show test graphs
    """df_calcs = pd.DataFrame(data=data_list, columns=debt_columns)
    df_calcs.plot()
    plt.show()"""

# TODO create pandas DF combining values to plot
# new_columns = src_data['parameters']['payments']['strategy']
# df_combined = pd.concat([df1, df2], axis=1)
# df_combined.plot()
# plt.show()

logger.debug("That's all folks")
print("\nThat's all folks")
