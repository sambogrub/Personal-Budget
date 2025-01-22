import sqlite3
import pytest
from unittest.mock import MagicMock
from contextlib import contextmanager

from personal_budget.table_schema import initialize_db_tables
from personal_budget.repository import AccountRepo, CategoryRepo
from personal_budget.model import Account, Category
from personal_budget.repository_controller import RepositoryController

@pytest.fixture
def setup_db_and_connection():
    conn = sqlite3.connect(":memory:") #want to make sure the test DB is in memory and not an actual DB, Keeping tests consistent
    mock_logger = MagicMock()

    initialize_db_tables(conn, mock_logger) #using this function to make sure it is using the actual table schema

    yield conn #making sure the connection is passed to the test function

    conn.close()

#------------ AccountRepo Tests-----------------
def test_create_account_entry(setup_db_and_connection):
    conn = setup_db_and_connection
    
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    accountrepo = AccountRepo(repo_controller, mock_logger)
    account = Account('Chase', 'Checking', balance=150.73)

    accountrepo.create_account_entry(account)

    with repo_controller.cursor_manager() as cursor:
        cursor.execute(
            "SELECT name, type, balance FROM accounts WHERE name = ?", ('Chase', ))
        row = cursor.fetchone()
        assert row == ('Chase', 'Checking', 150.73)

def test_get_account_entries(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    accountrepo = AccountRepo(repo_controller, mock_logger)
    account1 = Account('Chase', 'Checking', balance=150.73)
    account2 = Account('RBFCU', 'Checking', balance=195.80)
    account3 = Account('Chase', 'Savings', balance=1050.50)

    test_accounts = [(1, 'Chase', 'Checking', 150.73), (2, 'RBFCU', 'Checking', 195.80), (3, 'Chase', 'Savings', 1050.50)]

    accountrepo.create_account_entry(account1)
    accountrepo.create_account_entry(account2)
    accountrepo.create_account_entry(account3)

    accounts = accountrepo.get_all_account_entries()

    assert accounts == test_accounts

def test_get_account_by_id(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    accountrepo = AccountRepo(repo_controller, mock_logger)
    account1 = Account('Chase', 'Checking', balance=150.73)
    account2 = Account('RBFCU', 'Checking', balance=195.80)
    account3 = Account('Chase', 'Savings', balance=1050.50)

    accountrepo.create_account_entry(account1)
    accountrepo.create_account_entry(account2)
    accountrepo.create_account_entry(account3)

    account = accountrepo.get_account_by_id(2)

    assert account == (2, 'RBFCU', 'Checking', 195.80)

def test_update_account_entry(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    accountrepo = AccountRepo(repo_controller, mock_logger)

    account = Account('Chase', 'Checking', balance=150.73)
    
    accountrepo.create_account_entry(account)

    account.id = 1
    account.name = 'RBFCU'
    account.type = 'Savings'
    account.balance = 100.50

    new_account_info = (1, 'RBFCU', 'Savings', 100.50)

    accountrepo.update_account_entry(account)

    account_info = accountrepo.get_account_by_id(1)

    assert account_info == new_account_info


#----------------CategoryRepo tests -------------------
def test_create_category_info(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    categoryrepo = CategoryRepo(repo_controller, mock_logger)

    category = Category('Food')

    categoryrepo.create_category_entry(category)

    with repo_controller.cursor_manager() as cursor:
        cursor.execute("SELECT * FROM categories")
        category = cursor.fetchall()
        assert category == [(1, 'Food', None)]

def test_get_all_categories(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    categoryrepo = CategoryRepo(repo_controller, mock_logger)

    category1 = Category('Food')
    category2 = Category('Vehicle')
    category3 = Category('Groceries', 1)
    category4 = Category('Gas', 2)

    test_category_info = [(1, 'Food', None), (2, 'Vehicle', None), (3, 'Groceries', 1), (4, 'Gas', 2)]

    categoryrepo.create_category_entry(category1)
    categoryrepo.create_category_entry(category2)
    categoryrepo.create_category_entry(category3)
    categoryrepo.create_category_entry(category4)

    db_category_info = categoryrepo.get_all_categories()

    assert db_category_info == test_category_info

def test_get_category_by_id(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    categoryrepo = CategoryRepo(repo_controller, mock_logger)

    category1 = Category('Food')
    category2 = Category('Vehicle')
    category3 = Category('Groceries', 1)
    category4 = Category('Gas', 2)

    categoryrepo.create_category_entry(category1)
    categoryrepo.create_category_entry(category2)
    categoryrepo.create_category_entry(category3)
    categoryrepo.create_category_entry(category4)

    db_category = categoryrepo.get_category_by_id(3)

    assert db_category == (3, 'Groceries', 1)

def test_update_category(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    categoryrepo = CategoryRepo(repo_controller, mock_logger)

    category1 = Category('Food')
    category2 = Category('Vehicle')
  
    categoryrepo.create_category_entry(category1)
    categoryrepo.create_category_entry(category2)

    category2.id = 2
    category2.name = 'Takeout'
    category2.parent_id = 1

    categoryrepo.update_category(category2)

    db_category = categoryrepo.get_category_by_id(2)

    assert db_category == (2, 'Takeout', 1)

#--------------BudgetRepo Tests-----------------
