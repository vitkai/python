"""
Descr: time management records processing for QTimeRec software
@author: vitkai
Created: Sun May 20 2018 08:15
"""

import __main__ as main
import logging
import pandas as pd
import ruamel.yaml as yml
import codecs
# from functools import reduce
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

    # process csv related parameters
    global imp_columns, subst_month, subst_other, csv_sep, subst_items, stored_base_filename

    imp_columns = cfg['csv_parameters']['columns']
    subst_month = cfg['csv_parameters']['substs']['months']
    subst_items = cfg['csv_parameters']['substs']['items']
    subst_other = cfg['csv_parameters']['substs']['other']
    csv_sep = cfg['csv_parameters']['separator']
    stored_base_filename = cfg['stored_filename']
    logger.debug("Substs: \nColumns: {0} || \nMonths: {1} || \nOther: {2} || \nCSV Separator: {3} || \nItems: {4}".format(imp_columns, subst_month, subst_other, csv_sep, subst_items))

    #return src_dir, dst_dir


def imp_df(src_dir):
    """importing pandas dataframe from csv file"""

    src_dir = get_abs_path(src_dir, full_path)
    """
    if not path.isabs(src_dir):
        src_dir = full_path + '/' + src_dir
        logger.debug("Path is relative")
    logger.debug("Input dir is: {0}|| Full path is: {1}".format(src_dir, full_path))
    """

    df_imported = pd.read_csv(src_dir + "qtimerec_2018_03.csv", encoding='utf-8', sep=csv_sep, header=0, names=imp_columns)
    df_imported = df_imported.dropna()

    # substitute tracked items values
    df_imported[imp_columns[1]] = df_imported[imp_columns[1]].replace(subst_items, regex=True)
    df_imported[imp_columns[2]] = df_imported[imp_columns[2]].replace(subst_items, regex=True)

    # substitute months names
    df_imported[imp_columns[0]] = df_imported[imp_columns[0]].replace(subst_month, regex=True)
    df_imported[imp_columns[0]] = df_imported[imp_columns[0]].replace(subst_other, regex=True)

    # convert 1st column to date format
    df_imported[imp_columns[0]] = pd.to_datetime(df_imported[imp_columns[0]])

    logger.debug("DF imported from csv:\n{0}".format(df_imported.head()))

    return df_imported

def load_stored_base():
    """function to load all previously processed data"""

    global base_exists, base_filename#, stored_base_filename
    base_exists = False

    base_filename = get_abs_path(stored_base_filename, full_path)
    if path.exists(base_filename):
        base_exists = True

    logger.debug("Base exists: %s", base_exists)


def get_abs_path(src_path, fullpath):
    """Checks whether path is absolute or relative and returns absolute path"""

    if not path.isabs(src_path):
        src_path = fullpath + '/' + src_path
        logger.debug("Path was relative. Converted to '%s'", src_path)

    return src_path

# main starts here
logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

load_cfg()

load_stored_base()

df_imported = imp_df(inp_dir)

# add field Year and group by year
# TODO [START] move this block to a functions (process and write?)
df_imported['Year'] = df_imported[imp_columns[0]].dt.year
logger.debug("\nImported DF with 'Year' field added:\n{0}".format(df_imported.head()))

# find what years are included
years_count = df_imported['Year'].nunique()
logger.debug("Years entries:%s", years_count)

years_list = df_imported['Year'].unique()
logger.debug("Years list:%s", years_list)

# Create a Pandas Excel writer using XlsxWriter as the engine.
logger.debug("Saving to file: %s",base_filename)
writer = pd.ExcelWriter(base_filename, engine='xlsxwriter')

for yr in years_list:
    # filter to a separate DF by year
    logger.debug("Processing year:%s", yr)
    df_sheet = df_imported[df_imported['Year'] == yr]
    logger.debug("DF for the year:\n%s", df_sheet.head())
    # Write each dataframe to a different worksheet
    # TODO 1) update 'DATE' format since we do not need time there 2)remove index column 3) do we need to store 'Year' column?
    df_sheet.to_excel(writer, sheet_name=str(yr))

# Close the Pandas Excel writer and output the Excel file.
writer.save()
#writer.close()

#df_imported = df_imported.groupby('Year', as_index=True).agg({"Task":"sum"})
# TODO [END] move this block to a function


# TODO 1) export/store .xlsx file with years as sheet names
# TODO 2) imported file to be merged with stored file making sure that dates range was not in stored file before
# TODO 2) a) perhaps we need to store index of date ranges in a separate sheet?
# (/) TODO 3) add new field - year.
# TODO 3) a)Store data in separate sheets by year
# TODO 4) Reading stored data: a) list sheets b) number by years c) read into array of DFs

logger.debug("That's all folks")
print("That's all folks")
