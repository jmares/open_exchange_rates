import sqlite3
from sqlite3 import Error
from config import DB_FILE
import logging
from datetime import datetime
import time
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def get_log_file_mode(log_file):
    """
    Determine the file-mode for the log-file for weekday rotation

    Parameters:
    log_file (str): path for the log-file

    Returns: 
    string: file-mode append ('a') or write ('w')
    """
    now = datetime.now()
    # check if log-file exists 
    if os.path.isfile(log_file):
        # if the log-file exists, compare the modified date to the current date
        file_date = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(log_file)))
        if file_date == now.strftime("%Y-%m-%d"):
            # if the modified date equals the current date, set file-mode to append
            file_mode = 'a'
        else:
            # if the modified date is different (older), set file-mode to (over)write
            file_mode = 'w'
    else:
        # if the log-file doesn't exist, set file-mode to write
        file_mode = 'w'

    return file_mode


def create_table(conn, sql):
    """ create a table from the sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def main():

    create_tbl_currencies = """CREATE TABLE currencies (
        code    TEXT PRIMARY KEY NOT NULL,
        name    TEXT UNIQUE NOT NULL
        );"""

    create_tbl_rates = """CREATE TABLE rates_base_usd (
        date_time    TEXT NOT NULL,
        curr_code    TEXT NOT NULL,
        rate         REAL NOT NULL,
        PRIMARY KEY (date_time ASC, curr_code ASC),
        FOREIGN KEY (curr_code) REFERENCES currencies (code)
        );"""

    # other tables: daily_avg_base_eur and daily_avg_eur_base_currency

    # create a database connection
    conn = create_connection(DB_FILE)

    # create tables
    if conn is not None:
        create_table(conn, create_tbl_currencies)
        create_table(conn, create_tbl_rates)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()