"""Main module for the budget app"""

import sqlite3
from contextlib import contextmanager

import personal_budget.logger as logger

#-------Global variables--------
DB_NAME = 'budget_data.DB'


def db_connection(logger_: logger.logging.Logger) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(DB_NAME)
        logger_.info('Connection to DB established')
    except sqlite3.Error:
        logger_.exception('Error connecting to the database')
        raise
 
    return conn
    

def personal_budget():
    
    logger.configure_logger()
    log = logger.budget_logger()

    db_conn = db_connection(log)
    


     