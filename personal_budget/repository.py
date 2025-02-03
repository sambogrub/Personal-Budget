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
        
    def get_account_by_id(self, id) -> tuple:
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
    def __init__(self, controller, logger_: logger.logging.Logger):
        self.controller = controller
        self._logger = logger_

    def create_category_entry(self, category: model.Category):
        name = category.name
        parent_id = category.parent_id

        create_query = """
            INSERT INTO categories (name, parent_id)
            VALUES (?, ?)
            """

        with self.controller.cursor_manager() as cursor:
            cursor.execute(create_query, (name, parent_id))
            self._logger.info(f'Category {name}, with parent {parent_id} created')

    def get_all_categories(self) -> list[tuple]:
        get_query = """
            SELECT * FROM categories
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query)
            categories = cursor.fetchall()
            self._logger.info('All categories retrieved')
            return categories
        
    def get_category_by_id(self, id_) -> tuple:
        get_query = """
            SELECT * FROM categories
            WHERE id = ?
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query, (id_, ))
            category = cursor.fetchone()
            self._logger.info(f'Category {id_} retrieved')
            return category

    def update_category(self, category: model.Category):
        id_ = category.id
        name = category.name
        parent_id = category.parent_id

        update_query = """
            UPDATE categories
            SET name = ?, parent_id = ?
            WHERE id = ?
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(update_query, (name, parent_id, id_))
            self._logger.info(f"Category {name} updated")


class BudgetCategoryRepo:
    def __init__(self, controller, logger_: logger.logging.Logger):
        self.controller = controller
        self._logger = logger_

    def create_budgetcategory_entry(self, budgetcategory: model.BudgetCategory):
        name = budgetcategory.name
        type_ = budgetcategory.type
        budget_amount = budgetcategory.budget_amount
        remaining_amount = budgetcategory.remaining_amount
        period = budgetcategory.period
        created_at = budgetcategory.get_created_at_str()
        updated_at = budgetcategory.get_updated_at_str()
        is_active = budgetcategory.is_active
        parent_id = budgetcategory.parent_id
        category_id = budgetcategory.category_id

        values = (name, type_, budget_amount, remaining_amount, period, created_at, updated_at, is_active, parent_id, category_id)

        create_query = """
            INSERT INTO budget(
            name, type, budget_amount, remaining_amount, period, created_at,
            updated_at, is_active, parent_id, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

        with self.controller.cursor_manager() as cursor:
            cursor.execute(create_query, values)
            self._logger.info(f'Budget Category {name} created')

    def get_all_budgetcategories(self) -> list[tuple]:
        get_query = """
            SELECT * FROM budget
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query)
            bcategories = cursor.fetchall()
            self._logger.info('Retrieved all budget category entries')
            return bcategories
        
    def get_budgetcategory_by_id(self, id_) -> tuple:
        get_query = """
        SELECT * FROM budget
        WHERE id = ?
        """

        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query, (id_, ))
            bcategory = cursor.fetchone()
            self._logger.info(f'Retrieved budget category id {id_}')
            return bcategory

    def update_budgetcategory(self, budgetcategory: model.BudgetCategory):
        name = budgetcategory.name
        type_ = budgetcategory.type
        budget_amount = budgetcategory.budget_amount
        remaining_amount = budgetcategory.remaining_amount
        period = budgetcategory.period
        created_at = budgetcategory.get_created_at_str()
        updated_at = budgetcategory.get_updated_at_str()
        is_active = budgetcategory.is_active
        parent_id = budgetcategory.parent_id
        category_id = budgetcategory.category_id
        id_ = budgetcategory.id

        columns_dict = {'name': name,
                  'type': type_,
                  'budget_amount': budget_amount,
                  'remaining_amount': remaining_amount,
                  'period': period,
                  'created_at': created_at,
                  'updated_at': updated_at,
                  'is_active': is_active,
                  'parent_id': parent_id,
                  'category_id': category_id}

        keys_str_list = [key + ' = ?' for key in columns_dict]
        keys_str = ', '.join(keys_str_list)
        values = tuple(columns_dict.values()) + (id_, )

        update_query = f"""
            UPDATE budget
            SET {keys_str}
            WHERE id = ?"""
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(update_query, values)
            self._logger.info(f'Budget Category {id_} updated with {columns_dict}')

    def get_budgetcategory_list(self) -> list[tuple]:
        get_query = """
            SELECT id, name
            FROM budget
            """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query)
            bcategories = cursor.fetchall()
            return bcategories
        

class TransactionRepo:
    def __init__(self, controller, logger_: logger.logging.Logger):
        self.controller = controller
        self._logger = logger_

    def create_transaction_entry(self, transaction: model.Transaction):
        date = transaction.get_date_str()
        amount = transaction.amount
        account = transaction.account
        category = transaction.category
        budgetcategory = transaction.budgetcategory
        description = transaction.description
        type = transaction.type

        values = (date, amount, account, type, category, budgetcategory, description)

        create_query = """
                INSERT INTO transactions(
                date, amount, account_id, type, category_id, budget_id, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """

        with self.controller.cursor_manager() as cursor:
            cursor.execute(create_query, values)
            self._logger.info(f'Transaction in category {category} with amount ${amount}')

    def get_all_transactions(self):
        get_query = """
                SELECT * FROM transactions
                """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query)
            transactions = cursor.fetchall()
            self._logger.info('All transactions retrieved')
            return transactions
        
    def get_transaction_by_category(self, category_):
        get_query = """
                SELECT * FROM transactions
                WHERE category_id = ?
                """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query, (category_, ))
            transactions = cursor.fetchall()
            self._logger.info(f'Transacions from category {category_} retrieved')
            return transactions

    def get_transaction_by_budgetcategory(self, budgetcategory_):
        get_query = """
                SELECT * FROM transactions
                WHERE budget_id = ?
                """
        
        with self.controller.cursor_manager() as cursor:
            cursor.execute(get_query, (budgetcategory_, ))
            transactions = cursor.fetchall()
            self._logger.info(f'Transacions from budget category {budgetcategory_} retrieved')
            return transactions
        
    def get_transactions_by_date_range(self, start_date, end_date):
        pass
