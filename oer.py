import requests
import sqlite3
from sqlite3 import Error
import sys
import os
from config import OER_APP, OER_URL, DB_FILE, LOG_DIR
import logging
from datetime import datetime
import time

#dbconn = None

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    this_function = sys._getframe().f_code.co_name
    logging.debug(f"{this_function}: start")
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        logging.debug(f"{this_function}: connected to database {DB_FILE}")
        return conn
    except Error as e:
        logging.critical(f"{this_function}: could not connect to database - {e}")


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


def get_currencies():
    this_function = sys._getframe().f_code.co_name
    logging.debug(f"{this_function}: start")
    try:
        r = requests.get(OER_URL + 'currencies.json')
        data = r.json()
        return data
    except Exception as e:
        logging.error(f"{this_function}: could not download currencies - {e}")
        raise Exception(f"could not download currencies - {e}")


def get_rates():
    this_function = sys._getframe().f_code.co_name
    logging.debug(f"{this_function}: start")
    try:
        params = {'app_id': OER_APP}
        r = requests.get(OER_URL + 'latest.json', params)
        data = r.json()
        return data
    except Exception as e:
        logging.error(f"{this_function}: could not download rates - {e}")
        raise Exception(f"could not download rates - {e}")



def insert_currencies(currencies, dbconn):
    this_function = sys._getframe().f_code.co_name
    logging.debug(f"{this_function}: start")
    cur = dbconn.cursor()

    sql = '''REPLACE INTO currencies (code, name) VALUES (?, ?)'''
    
    for symbol, name in currencies.items():
        try:
            cur.execute(sql, (symbol, name))
            dbconn.commit()
        except Exception as e:
            logging.error(f"{this_function} - error with symbol {symbol} and name {name}: {e}")



def insert_rates(data, dbconn):
    this_function = sys._getframe().f_code.co_name
    logging.debug(f"{this_function}: start")
    cur = dbconn.cursor()

    sql = '''REPLACE INTO rates_base_usd (date_time, curr_code, rate) VALUES (?, ?, ?)'''
    date_time = datetime.fromtimestamp(int(data['timestamp']))
    rates = data['rates']

    for code, rate in rates.items():
        try:
            cur.execute(sql, (date_time, code, float(rate)))
            dbconn.commit()
        except Exception as e:
            print(f'Error with {code}, {date_time} and {rate}: ' + str(e))


def main():
    this_function = sys._getframe().f_code.co_name
    start_time = time.time()
    now = datetime.now()
    # create log-file per weekday: oer_Wed.log
    try: 
        log_file = LOG_DIR + 'oer_' + now.strftime('%a') + '.log'
        log_level = logging.INFO
        file_mode = get_log_file_mode(log_file)
        logging.basicConfig(filename=log_file, filemode=file_mode, format='%(asctime)s - %(levelname)s : %(message)s', level=log_level)
        logging.info(f"{this_function}: start")
        print(log_file, log_level, file_mode)
    except Exception as e:
        print(e)

    try:
        dbconn = create_connection()
        data = get_currencies()
        insert_currencies(data, dbconn)
        data = get_rates()
        insert_rates(data, dbconn)
    except Exception as e:
        logging.error(f"{this_function}: {e}")

    end_time = time.time()
    duration = str(round(end_time - start_time, 3))
    logging.info(f"{this_function}: time needed for script {duration} seconds")
    logging.info(f"{this_function}: ending execution\n")
    print(f"duration: {duration}s")


if __name__ == '__main__':
    main()