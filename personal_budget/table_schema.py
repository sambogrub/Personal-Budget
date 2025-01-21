"""Module for the creation of the appropriate tables for the database"""

import sqlite3

import personal_budget.logger as logger


def initialize_db_tables(conn: sqlite3.Connection, logger_):
    account_query = """
        CREATE TABLE accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        balance DECIMAL
        )"""

    category_query = """
        CREATE TABLE categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES categories (id)
        )"""

    budget_query = """
        CREATE TABLE budget(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        budget_amount DECIMAL NOT NULL,
        remaining_amount DECIMAL,
        period TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        is_active INTEGER NOT NULL,
        parent_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES budget (id),
        FOREIGN KEY (category_id) REFERENCES categories (id)
        )"""

    transaction_query = """
        CREATE TABLE transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount DECIMAL NOT NULL,
        account_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        category_id INTEGER,
        budget_id INTEGER,
        description TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts (id),
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (budget_id) REFERENCES budget (id)
        )"""
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(account_query)
        cursor.execute(category_query)
        cursor.execute(budget_query)
        cursor.execute(transaction_query)
        conn.commit()
        logger_.info('Database tables created')
    except sqlite3.IntegrityError:
        conn.rollback()
        logger_.exception('SQLite error:')
    except Exception:
        conn.rollback()
        logger_.exception('SQLite error:')
        raise
    finally:
        if cursor is not None:
            cursor.close()