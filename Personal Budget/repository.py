"""This is the database handler and repository"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager

def init_database_tables():
    