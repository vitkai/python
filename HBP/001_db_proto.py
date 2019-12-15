"""
Descr: db module prototype
@author: vitkai
Created: Sun Dec 15 2019 13:05 MSK
"""
import __main__
import logging
from os import path
import sqlite3
from sqlite3 import Error

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

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        msg = "sqlite3.version = {0}".format(sqlite3.version)
        print(msg)
        logger.debug(msg)
    except Error as e:
        print(e)
        logger.error(e)
            
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        logger.error(e)

# main starts here
def main():
    global logger
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    
    # db statements
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
 
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(full_path + '\\' + 'hbp.db')

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
 
        # create tasks table
        create_table(conn, sql_create_tasks_table)

    logger.debug("That's all folks")
    print("\nThat's all folks")

if __name__ == "__main__":
    main()