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
import datetime
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
        df_imported[imp_columns[0]] = pd.to_datetime(df_imported[imp_columns[0]])#, format="%Y-%m-%d")

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

        # load dict keys into list
        stored_base_df_years = list(stored_base_df.keys())
        logger.debug("Base years-keys: {0}".format(stored_base_df_years))

        for idx, yr in enumerate(stored_base_df_years):
            str_yr = str(yr)
            stored_base_df_years[idx] = str_yr
            stored_base_df[str_yr] = stored_base_df.pop(yr)
            stored_base_df[str_yr]["Date"] = pd.to_datetime(stored_base_df[str_yr]["Date"])#, format = "%Y-%m-%d")

        """
        try:
            stored_base_df_years[idx] = str(yr)
        except Exception as e:
            msg = "Error processing stored database sheets. Ignoring loaded base."
            pprint(msg)
            pprint(e)
            logger.error(msg)
            logger.error(e)
            base_exists = False
        finally:
            pass
        """

    logger.debug("Loaded existing database:{0}".format(base_filename))
    print("Loaded existing database:", base_filename)


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

    years_list = list(df_to_proc['Year'].unique())
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
        yr_str = str(yr)
        dict_df[yr_str] = df_sheet
        logger.debug("DF with key '{0}': \n {1}".format(yr, dict_df[yr_str].head()))

    return dict_df, years_list


def write_base():
    """Stores final data into base workbook"""
    if not base_exists:
        pprint("Base does not exist. Nothing to save...")
        logger.info("Base does not exist. Nothing to save...")
        # we need some checks before writing new data -- see TODO 5)
    else:
        pprint("Saving base file...")
        logger.info("Saving base file...")
        # add field Year and group by year

        # make a backup if file exists
        if path.exists(base_filename):
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d_%H-%M")
            copy2(base_filename, path.splitext(base_filename)[0] + '_' + now + path.splitext(base_filename)[1])

        writer = pd.ExcelWriter(base_filename, engine='xlsxwriter', date_format='yyyy-mm-dd', datetime_format='yyyy-mm-dd')

        # cycle through years in base dict of DFs
        for yr in stored_base_df_years:
            yr_str = str(yr)
            logger.debug("Saving year:%s", yr)
            df_sheet = stored_base_df[yr_str]
            logger.debug("\n{0}".format(df_sheet.head()))
            # Write each dataframe to a different worksheet
            df_sheet.to_excel(writer, sheet_name=yr_str, index=False)

        # Close the Pandas Excel writer and output the Excel file.
        try:
            writer.save()
        except Exception as e:
            pprint(e)
            logger.error("Saving error:{0}".format(e))
        finally:
            writer.close()

# (!) TODO need to fix issues with loaded base
# (!) TODO 1) -- when merging items are being duplicated in output base
# (+) TODO 1) a) (possibly need to update base write -- (/) not guilty)
# (/) TODO 2) -- Date field in saved file contains unwanted time 2018-05-31 00:00:00
# (/) TODO 3) on base init for some reason base was not merged with May 2018
# (/) TODO 3) a) 2nd merged_df misses required dates
def merge_loaded_data(inp_df):
    """Checks imported data against loaded base
    if base does not present, will work on existing data set"""
    # check for years in imported DF (see current write_base version)
    # cycle through years in imported DF
    # compare date range by year in imported DF vs stored base
    # remove duplicates in imported DF
    # merge data with base
    logger.debug("{0}{1}merge_loaded_data() call{1}{0}".format('*'*10, '-'*10))

    global stored_base_df_years
    #stored_base_df_years = list(stored_base_df_years)

    inp_df, inp_yrs = split_df_by_years(inp_df)
    # cycle through years in input DF
    clmns = ["Date"]
    for yr in inp_yrs:
        yr_idx = str(yr)
        #yr_idx = yr
        inp_year_df = pd.DataFrame(inp_df[yr_idx])
        if yr_idx in stored_base_df_years:
            # check for duplicates
            logger.debug("'{0}' found in base years".format(yr))
            # get list of unique dates
            #inp_year_df = pd.DataFrame(inp_df[yr])
            #year_dates_df = inp_year_df["Date"]

            inp_dates_wo_dups = pd.DataFrame(inp_year_df["Date"].unique())#drop_duplicates()
            inp_dates_wo_dups.columns = clmns
            logger.debug("Input dates - no duplicates:\n{0}\n...\n{1}".format(inp_dates_wo_dups.head(), inp_dates_wo_dups.tail()))

            base_dates = pd.DataFrame(stored_base_df[yr_idx]["Date"].unique())
            base_dates.columns = clmns
            logger.debug("Base dates - no duplicates:\n{0}\n...\n{1}".format(base_dates.head(), base_dates.tail()))

            # filter analyzed dates vs base dates excluding those in base
            # should stay only dates that are not in the base
            # TODO this check has to be fixed, as now it returns values that are already in the base, and should be skipped
            # TODO this issue creates duplicates
            merged_df = inp_dates_wo_dups.loc[~inp_dates_wo_dups["Date"].isin(base_dates["Date"])]
            merged_df["Date"] = pd.to_datetime(merged_df["Date"], format="%Y-%m-%d")
            logger.debug("merged_df:\n{0}".format(merged_df.head()))

            # apply filtered dates to analyzed DF
            inp_year_all_dates_df = pd.DataFrame(inp_year_df["Date"])
            inp_year_all_dates_df["Date"] = pd.to_datetime(inp_year_all_dates_df["Date"], format="%Y-%m-%d")
            merged_df = inp_year_df.loc[inp_year_all_dates_df["Date"].isin(merged_df["Date"])]
            merged_df["Date"] = pd.to_datetime(merged_df["Date"], format="%Y-%m-%d")
            logger.debug("2nd merged_df:\n{0}\n...\n{1}".format(merged_df.head(), merged_df.tail()))

            # merge base and new dates
            stored_base_df[yr_idx]["Date"] = pd.to_datetime(stored_base_df[yr_idx]["Date"], format="%Y-%m-%d")
            stored_base_df[yr_idx] = pd.concat([merged_df, stored_base_df[yr_idx]]).sort_values(['Date'], ascending=True).reset_index(drop=True)
            logger.debug("stored_base_df[yr]:\n{0}\n...\n{1}".format(stored_base_df[yr_idx].head(), stored_base_df[yr_idx].tail()))

        else:
            # just add new year to base
            stored_base_df[yr_idx] = inp_year_df
            stored_base_df_years.append(yr_idx)
            #stored_base_df_years = stored_base_df_years + yr
            stored_base_df_years.sort()
            msg = "Base updated with year:{0}".format(yr_idx)
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

    stored_base_df_years = list(stored_base_df_years)
    for idx, yr in enumerate(stored_base_df_years):
        #stored_base_df_years[idx] = int(yr)
        yr_str = str(yr)
        stored_base_df_years[idx] = yr_str
        #stored_base_df[yr_str] = stored_base_df.pop(yr)

    pprint("Base initialized using loaded file")
    logger.info("Base initialized using loaded file")


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

# save base file
write_base()

logger.debug("That's all folks")
pprint("That's all folks")
