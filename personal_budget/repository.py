"""This is the database handler and repository"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager

from personal_budget.table_schema import initialize_db_tables
import personal_budget.model as model
import personal_budget.logger as logger



class AccountRepo:
    def __init__(self, controller, logger_: logger.logging.Logger):
        self.controller = controller
        self._logger = logger_

    def create_account_entry(self, account: model.Account):
        name = account.name
        type = account.type
        balance = account.balance

        save_query = """
            INSERT INTO accounts (name, type, balance)
            VALUES (?, ?, ?)
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(save_query, (name, type, balance))
            self._logger.info(f"Account data saved for {name}, with type: {type} and balance: {balance}")
    
    def get_all_account_entries(self) -> list[tuple]:
        get_query = """
            SELECT * FROM accounts
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query)
            accounts = cursor.fetchall()
            self._logger.info("All account retrieved")
            return accounts
        
    def get_account_by_id(self, id):
        get_query = """
            SELECT * FROM accounts
            WHERE id = ?
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query, (id, ))
            account = cursor.fetchone()
            self._logger.info(f"Account id: {id} retrieved")
            return account
        
    def update_account_entry(self, account: model.Account):
        name = account.name
        type = account.type
        balance = account.balance
        id_ = account.id
        
        update_query = """
            UPDATE accounts
            SET name = ?, type = ?, balance = ?
            WHERE id = ?
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(update_query, (name, type, balance, id_))
            self._logger.info(f"Account id: {id} updated with name: {name}, type: {type}, and balance: {balance}")
        

class CategoryRepo:
    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection


class BudgetCategoryRepo:
    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection


class TransactionRepo:
    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection