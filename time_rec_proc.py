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
import tempfile
# from functools import reduce
from os import path, listdir, remove#, makedirs
from shutil import copy2
from pprint import pprint#,pformat


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

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-'*10 + '='*10 + '-'*10 + "\n"))

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


def imp_df(filename):
    """importing pandas dataframe from csv file"""

    tmp_file = tempfile.gettempdir() + '/time_rec.tmp'
    logger.debug("Temporary file:{0}".format(tmp_file))

    copy2(filename, tmp_file)
    file_read_err = False
    try:
        df_imported = pd.read_csv(tmp_file, encoding='utf-8', sep=csv_sep, header=0, names=imp_columns)
    except Exception as e:
        pprint(e)
        logger.error(e)
        df_imported = pd.DataFrame()
        file_read_err = True
    finally:
        remove(tmp_file)

    if not file_read_err:
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

    global base_exists, base_filename, stored_base_df_years, stored_base_df
    base_exists = False

    base_filename = get_abs_path(stored_base_filename, full_path)
    if path.exists(base_filename):
        base_exists = True
        stored_base_df = pd.read_excel(base_filename, None)
        stored_base_df_years = list(stored_base_df.keys())
        logger.debug("DF keys: {0}".format(stored_base_df_years))
        logger.debug("DF type:{0} | DF with key '{1}': \n {2}".format(type(stored_base_df[stored_base_df_years[0]]), stored_base_df_years[0], stored_base_df[stored_base_df_years[0]].head()))

    logger.debug("Base exists: %s", base_exists)


def get_abs_path(src_path, fullpath):
    """Checks whether path is absolute or relative and returns absolute path"""

    if not path.isabs(src_path):
        src_path = fullpath + '/' + src_path
        logger.debug("Path was relative. Converted to '%s'", src_path)

    return src_path


def split_df_by_years(df_to_proc):
    """Checking DataFrame for years and splitting it into dict by years
    :returns DF splitted by years and years list"""

    df_to_proc['Year'] = df_to_proc[imp_columns[0]].dt.year
    #logger.debug("\nImported DF with 'Year' field added:\n{0}".format(df_to_proc.head()))

    # find what years are included
    years_count = df_to_proc['Year'].nunique()
    logger.debug("Years entries:%s", years_count)

    years_list = df_to_proc['Year'].unique()
    logger.debug("Years list:%s", years_list)

    # convert DF to ordered dict of dataframes
    dict_df = {}
    for yr in years_list:
        # filter to a separate DF by year
        logger.debug("Processing year:%s", yr)
        df_sheet = df_to_proc[df_to_proc['Year'] == yr]
        logger.debug("DF for the year:\n%s", df_sheet.head())
        # get rid of "Year" column
        df_sheet = df_sheet.drop('Year', 1)
        # convert to date only format
        df_sheet[imp_columns[0]] = df_sheet[imp_columns[0]].dt.date
        # add each sheet to dict
        dict_df[yr] = df_sheet

        logger.debug("DF with key '{0}': \n {1}".format(yr, dict_df[yr].head()))

    return dict_df, years_list


# TODO fix write_base processing
def write_base(df_to_save):
    """Stores final data into base workbook"""
    if base_exists:
        pprint("Base exists. Will not re-write it for now")
        # we need some checks before writing new data -- see TODO 5)
    else:
        pprint("Base does not exist. Will write it now")
        # add field Year and group by year

        df_to_save, years_list = split_df_by_years(df_to_save)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        logger.debug("Saving to file: %s", base_filename)
        writer = pd.ExcelWriter(base_filename, engine='xlsxwriter', date_format='yyyy-mm-dd')

        for yr in years_list:
            # filter to a separate DF by year
            logger.debug("Processing year:%s", yr)
            df_sheet = df_to_save[df_to_save['Year'] == yr]
            logger.debug("DF for the year:\n%s", df_sheet.head())
            # get rid of "Year" column
            df_sheet = df_sheet.drop('Year', 1)
            # convert to date only format
            df_sheet[imp_columns[0]] = df_sheet[imp_columns[0]].dt.date
            # df_sheet[imp_columns[0]] = df_sheet.loc[:, imp_columns[0]].dt.date
            # Write each dataframe to a different worksheet
            df_sheet.to_excel(writer, sheet_name=str(yr), index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        # writer.close()

def merge_loaded_data(inp_df):
    """Checks imported data against loaded base
    if base does not present, will work on existing data set"""
    # check for years in imported DF (see current write_base version)
    # cycle through years in imported DF
    # compare date range by year in imported DF vs stored base
    # remove duplicates in imported DF
    # merge data with base
    logger.debug("merge_loaded_data() call")
    global stored_base_df_years
    inp_df, inp_yrs = split_df_by_years(inp_df)
    # cycle through years in input DF
    clmns = ["Date"]
    for yr in inp_yrs:
        year_df = pd.DataFrame(inp_df[yr])
        if yr in stored_base_df_years:
            # check for duplicates
            logger.debug("'{0}' found in base years".format(yr))
            # get list of unique dates
            #year_df = pd.DataFrame(inp_df[yr])
            #year_dates_df = year_df["Date"]

            inp_dates_wo_dups = pd.DataFrame(year_df["Date"].unique())#drop_duplicates()
            inp_dates_wo_dups.columns = clmns
            logger.debug("Input dates - no duplicates:\n{0}\n...\n{1}".format(inp_dates_wo_dups.head(), inp_dates_wo_dups.tail()))

            base_dates = pd.DataFrame(stored_base_df[yr]["Date"].unique())#drop_duplicates()
            base_dates.columns = clmns

            # filter analyzed dates vs base dates excluding those in base
            merged_df = inp_dates_wo_dups.loc[~inp_dates_wo_dups["Date"].isin(base_dates["Date"])]
            logger.debug("merged_df:\n{0}".format(merged_df.head()))

            # apply filtered dates to analyzed DF
            merged_df = year_df.loc[year_df["Date"].isin(merged_df["Date"])]
            logger.debug("2nd merged_df:\n{0}\n...\n{1}".format(merged_df.head(), merged_df.tail()))

            # merge base and new dates
            stored_base_df[yr] = pd.concat([merged_df, stored_base_df[yr]]).sort_values(['Date'], ascending=True).reset_index(drop=True)
            logger.debug("stored_base_df[yr]:\n{0}\n...\n{1}".format(stored_base_df[yr].head(), stored_base_df[yr].tail()))

        else:
            # just add new year to base
            stored_base_df[yr] = year_df
            stored_base_df_years = list(stored_base_df_years)
            stored_base_df_years.append(yr)
            stored_base_df_years.sort()
            msg = "Base updated with year:{0}".format(yr)
            print(msg)
            logger.info(msg)
            logger.debug("base years: {0}".format(stored_base_df_years))

        #logger.debug("new base state: \n{0}".format(stored_base_df))

def init_base(inp_df):
    """When base does not exist create it to work with it the same way as if we loaded it"""
    #inp_df, yrs_list = split_df_by_years(inp_df)
    # save it, load it and we have a base :)
    global stored_base_df, stored_base_df_years, base_exists
    stored_base_df, stored_base_df_years = split_df_by_years(inp_df)
    base_exists = True


# main starts here
logger = logging_setup()

# get script path
full_path, filename = path.split(__file__)
logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

load_cfg()

load_stored_base()

for imp_file in listdir(get_abs_path(inp_dir, full_path)):
    imp_file = get_abs_path(inp_dir + imp_file, full_path)
    msg = "{0}\nReading {1}\n{0}".format('-'*10, imp_file)
    print(msg)
    logger.info("\n" + msg)
    imported_csv = imp_df(imp_file)

    if imported_csv.empty:
        pprint("Read empty data")
        logger.info("Read empty data")
    else:
        if not base_exists:
            init_base(imported_csv)
        else:
            merge_loaded_data(imported_csv)
    # if base_exists:
        # [Compare] we comparing all imported data for existing date ranges to avoid duplications
    # else:
        # we work in the mode of base creation
        #  - forming new base from imported data and doing [Compare] steps for every newly loaded data
        # this situation is only possible when we run for the very 1st time -- that's why nothing is stored as base yet

    #write_base(imported_csv)

# df_imported = df_imported.groupby('Year', as_index=True).agg({"Task":"sum"})

# (+) TODO 1) export/store .xlsx file with years as sheet names -- see #3)
# (!) TODO 2) imported file to be merged with stored file making sure that dates range was not in stored file before
# (x) TODO 2) a) perhaps we need to store index of date ranges in a separate sheet? See 3)
# (/) TODO 3) add new field - year.
# (+) TODO 3) a)Store data in separate sheets by year
# (!) TODO 3) b) before storing need to make sure there are no duplicates in imported dataframes
# (+) TODO 4) Reading stored data: a) list sheets b) number by years c) read into array of DFs (ordered dict)
# (!) TODO 5) all imported data should be checked against already stored data for duplicates - see 2)a)

logger.debug("That's all folks")
pprint("That's all folks")
