import sqlite3
import pytest
from unittest.mock import MagicMock
from contextlib import contextmanager
from datetime import datetime

from personal_budget.table_schema import initialize_db_tables
from personal_budget.repository import AccountRepo, CategoryRepo, BudgetCategoryRepo, TransactionRepo
from personal_budget.model import Account, Category, BudgetCategory, Transaction
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
def test_create_budgetcategory_entry(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)

    budgetcategoryrepo = BudgetCategoryRepo(repo_controller, mock_logger)

    now = datetime.now()
    

    budgetcateory = BudgetCategory('food', 'income', now, now, 100.0, 56.00, 'monthly', True, None, None, None)
    now_str = budgetcateory.get_created_at_str()

    budgetcategoryrepo.create_budgetcategory_entry(budgetcateory)

    with repo_controller.cursor_manager() as cursor:
        cursor.execute('SELECT * FROM budget')
        b_category = cursor.fetchone()
        assert b_category == (1, 'food', 'income', 100.00, 56.00, 'monthly', now_str, now_str, True, None, None)

def test_get_all_budget_categories(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()
    repo_controller = RepositoryController(conn, mock_logger)
    budgetcategoryrepo = BudgetCategoryRepo(repo_controller, mock_logger)

    now = datetime.now()

    budgetcategory1 = BudgetCategory('food', 'expense', now, now, 1000.0, 560.00, 'monthly', True, None, None, None)
    budgetcategory2 = BudgetCategory('grocery', 'expense', now, now, 100.0, 56.00, 'monthly', True, 1, None, None)

    now_str = budgetcategory1.get_created_at_str()

    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory1)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory2)

    bcategories = budgetcategoryrepo.get_all_budgetcategories()

    assert bcategories == [(1, 'food', 'expense', 1000.00, 560.00, 'monthly', now_str, now_str, True, None, None),
                           (2, 'grocery', 'expense', 100.00, 56.00, 'monthly', now_str, now_str, True, 1, None)]

def test_get_budgetcategory_by_id(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)
    now = datetime.now()
    budgetcategoryrepo = BudgetCategoryRepo(repo_controller, mock_logger)

    budgetcategory1 = BudgetCategory('food', 'expense', now, now, 1000.00, 560.00, 'monthly', True, None, None, None)
    budgetcategory2 = BudgetCategory('grocery', 'expense', now, now, 100.00, 56.00, 'monthly', True, 1, None, None)
    budgetcategory3 = BudgetCategory('gas', 'expense', now, now, 50.00, 50.00, 'monthly', True, None, None, None)
    budgetcategory4 = BudgetCategory('Lacie income', 'income', now, now, 1200.0, 1200.00, 'monthly', True, None, None, None)

    now_str = budgetcategory1.get_created_at_str()

    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory1)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory2)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory3)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory4)

    db_budgetcategory = budgetcategoryrepo.get_budgetcategory_by_id(2)

    assert db_budgetcategory == (2, 'grocery', 'expense', 100.00, 56.00, 'monthly', now_str, now_str, True, 1, None)

def test_update_budgetcategory(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)
    budgetcategoryrepo = BudgetCategoryRepo(repo_controller, mock_logger)

    now = datetime.now()

    # Create an initial budget category entry
    budgetcategory = BudgetCategory('food', 'expense', now, now, 500.00, 200.00, 'monthly', True, None, None, None)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory)

    # Retrieve the created entry to get the assigned ID
    budgetcategory_from_db = budgetcategoryrepo.get_all_budgetcategories()
    assert len(budgetcategory_from_db) == 1

    budgetcategory.id = budgetcategory_from_db[0][0]  # Assign ID from DB

    # Update budget category details
    budgetcategory.name = 'groceries'
    budgetcategory.type = 'expense'
    budgetcategory.budget_amount = 600.00
    budgetcategory.remaining_amount = 250.00
    budgetcategory.period = 'weekly'
    budgetcategory.is_active = False

    # Perform the update
    budgetcategoryrepo.update_budgetcategory(budgetcategory)

    # Retrieve and assert the updated data
    updated_category = budgetcategoryrepo.get_budgetcategory_by_id(budgetcategory.id)
    assert updated_category == (
        budgetcategory.id,
        'groceries',
        'expense',
        600.00,
        250.00,
        'weekly',
        budgetcategory.get_created_at_str(),
        budgetcategory.get_updated_at_str(),
        False,
        None,
        None
        )
    
def test_get_budgetcategory_list(setup_db_and_connection):
    conn = setup_db_and_connection
    mock_logger = MagicMock()

    repo_controller = RepositoryController(conn, mock_logger)
    budgetcategoryrepo = BudgetCategoryRepo(repo_controller, mock_logger)

    now = datetime.now()

    # Create multiple budget category entries
    budgetcategory1 = BudgetCategory('food', 'expense', now, now, 500.00, 200.00, 'monthly', True, None, None, None)
    budgetcategory2 = BudgetCategory('rent', 'expense', now, now, 1000.00, 0.00, 'monthly', True, None, None, None)

    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory1)
    budgetcategoryrepo.create_budgetcategory_entry(budgetcategory2)
    # Retrieve the list of budget categories

    categories_list = budgetcategoryrepo.get_budgetcategory_list()

    # Assert expected values
    assert len(categories_list) == 2
    assert categories_list[0][1] == 'food'
    assert categories_list[1][1] == 'rent'


#--------------Transaction Repository-----------------
def test_create_transaction_entry(setup_db_and_connection):
    """Test creating a transaction entry."""
    conn = setup_db_and_connection
    mock_logger = MagicMock()
    transaction_repo = TransactionRepo(conn, mock_logger)
    now = datetime.now()
    transaction = Transaction(
        date=now, amount=100.50, account=1, category=2, budgetcategory=3, description="Groceries", type="expense"
    )

    transaction_repo.create_transaction_entry(transaction)

    transactions = transaction_repo.get_all_transactions()
    assert len(transactions) == 1
    assert transactions[0][1] == transaction.get_date_str()
    assert transactions[0][2] == transaction.amount
    assert transactions[0][3] == transaction.account
    assert transactions[0][4] == transaction.type
    assert transactions[0][5] == transaction.category
    assert transactions[0][6] == transaction.budgetcategory
    assert transactions[0][7] == transaction.description

def test_get_all_transactions(setup_db_and_connection):
    """Test retrieving all transactions."""
    conn = setup_db_and_connection
    mock_logger = MagicMock()
    transaction_repo = TransactionRepo(conn, mock_logger)
    now = datetime.now()
    transaction1 = Transaction(
        date=now, amount=50.00, account=1, category=2, budgetcategory=3, description="Gas", type="expense"
    )
    transaction2 = Transaction(
        date=now, amount=200.00, account=2, category=3, budgetcategory=4, description="Salary", type="income"
    )

    transaction_repo.create_transaction_entry(transaction1)
    transaction_repo.create_transaction_entry(transaction2)

    transactions = transaction_repo.get_all_transactions()
    assert len(transactions) == 2
    assert {transactions[0][2], transactions[1][2]} == {50.00, 200.00}

def test_get_transaction_by_category(setup_db_and_connection):
    """Test retrieving transactions by category."""
    conn = setup_db_and_connection
    mock_logger = MagicMock()
    transaction_repo = TransactionRepo(conn, mock_logger)
    now = datetime.now()
    transaction1 = Transaction(
        date=now, amount=75.00, account=1, category=2, budgetcategory=3, description="Dining", type="expense"
    )
    transaction2 = Transaction(
        date=now, amount=120.00, account=1, category=3, budgetcategory=4, description="Shopping", type="expense"
    )

    transaction_repo.create_transaction_entry(transaction1)
    transaction_repo.create_transaction_entry(transaction2)

    category_transactions = transaction_repo.get_transaction_by_category(2)
    assert len(category_transactions) == 1
    assert category_transactions[0][2] == 75.00
    assert category_transactions[0][5] == 2

def test_get_transaction_by_budgetcategory(setup_db_and_connection):
    """Test retrieving transactions by budget category."""
    conn = setup_db_and_connection
    mock_logger = MagicMock()
    transaction_repo = TransactionRepo(conn, mock_logger)
    now = datetime.now()
    transaction1 = Transaction(
        date=now, amount=30.00, account=1, category=2, budgetcategory=3, description="Coffee", type="expense"
    )
    transaction2 = Transaction(
        date=now, amount=200.00, account=1, category=3, budgetcategory=4, description="Books", type="expense"
    )

    transaction_repo.create_transaction_entry(transaction1)
    transaction_repo.create_transaction_entry(transaction2)

    budget_transactions = transaction_repo.get_transaction_by_budgetcategory(3)
    assert len(budget_transactions) == 1
    assert budget_transactions[0][2] == 30.00
    assert budget_transactions[0][6] == 3