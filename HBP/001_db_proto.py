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

def db_create_connection(db_file):
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


def db_create_table(conn, db_create_table_sql):
    """ create a table from the db_create_table_sql statement
    :param conn: Connection object
    :param db_create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(db_create_table_sql)
    except Error as e:
        print(e)
        logger.error(e)
        
        
def db_create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def db_create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def db_init_tables(conn):
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
                                
    """
    -- Transaction_Records:
		ID|Date|Sum|CCY|Category|Content|Addition date|Upd date
	--Categories:
		ID|Category
	--Currencies:
		ID|CCY
    """

    sql_create_category_table = """ CREATE TABLE IF NOT EXISTS Category (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_ccy_table = """ CREATE TABLE IF NOT EXISTS Currency (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_tr_records_table = """ CREATE TABLE IF NOT EXISTS Tr_Records (
                                        id integer PRIMARY KEY,
                                        tr_date text NOT NULL,
                                        tr_sum integer NOT NULL,
                                        ccy_id integer NOT NULL,
                                        category_id integer NOT NULL,
                                        content text NOT NULL,
                                        add_date text NOT NULL,
                                        upd_date text NOT NULL,
                                        FOREIGN KEY (ccy_id) REFERENCES Currency (id),
                                        FOREIGN KEY (category_id) REFERENCES Category (id)
                                    ); """

    
    # create tables
    if conn is not None:
        # create projects table
        db_create_table(conn, sql_create_projects_table)
 
        # create tasks table
        db_create_table(conn, sql_create_tasks_table)
        
        # create transaction related tables
        db_create_table(conn, sql_create_category_table)
        db_create_table(conn, sql_create_ccy_table)
        db_create_table(conn, sql_create_tr_records_table)


def db_init_data(conn):
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        project_id = db_create_project(conn, project)
 
        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
 
        # create tasks
        db_create_task(conn, task_1)
        db_create_task(conn, task_2)
    

def db_update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def db_delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    
    
def db_delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def db_select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def db_select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
        

# main starts here
def main():
    global logger
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    
    # create a database connection
    conn = db_create_connection(full_path + '\\' + 'hbp.db')

    db_init_tables(conn)
    db_init_data(conn)
    
    with conn:
        # db_update_task(conn, (2, '2015-01-04', '2015-01-06', 2))
        # db_delete_task(conn, 2);
        # db_delete_all_tasks(conn);
        
        print("1. Query task by priority:")
        db_select_task_by_priority(conn, 1)
 
        print("2. Query all tasks")
        db_select_all_tasks(conn)
 
 
    logger.debug("That's all folks")
    print("\nThat's all folks")

if __name__ == "__main__":
    main()
    
# TODO: 
# 1. replace individual db_ functions with general SQL processing one
# 2. + add SQL statement generation in a separate function
# After quick research I doubt it is necessary to do 1 and 2