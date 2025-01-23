import pytest
from datetime import datetime

from personal_budget.model import Transaction, Account, Category, BudgetCategory
from personal_budget.config import DATETIME_STR_FORMAT

def test_transaction_initialization():
    now = datetime.now()
    transaction = Transaction(now, 32.48, 1, 3, 'van gas', 40, 'expense')
    assert transaction.date == now
    assert transaction.amount == 32.48
    assert transaction.account == 1
    assert transaction.category == 3
    assert transaction.description == 'van gas'
    assert transaction.id == 40
    assert transaction.type == 'expense'

@pytest.mark.parametrize(
    "attribute, value",
    [
        ("date", datetime.now()),
        ("amount", 100.50),
        ("account", 1),
        ("category", 2),
        ("description", "Test description"),
        ('id', 3),
    ]
)
def test_transaction_setters_and_getters(attribute, value):
    transaction = Transaction(datetime.now(), 50.25)
    setattr(transaction, attribute, value)  
    assert getattr(transaction, attribute) == value  


def test_account_initialization():
    account = Account('RBFCU', 'checking', 3, 10.75)
    assert account.name == 'RBFCU'
    assert account.type == 'checking'
    assert account.id == 3
    assert account.balance == 10.75

@pytest.mark.parametrize(
    "attribute, value",
    [
        ('name', 'Chase Checking'),
        ('type', 'Checking'),
        ('balance', 135.75),
        ('id', 3),
    ]
)
def test_account_setters_and_getters(attribute, value):
    account = Account('RBFCU', 'savings')
    setattr(account, attribute, value)
    assert getattr(account, attribute) == value


def test_category_initialization():
    category = Category('groceries', 1, 2)
    assert category._id == 2
    assert category.name == 'groceries'
    assert category._parent_id == 1

@pytest.mark.parametrize(
    'attribute, value',
    [
        ('name', 'gas'),
        ('id', 3),
    ]
)
def test_category_setters_and_getters(attribute, value):
    category = Category(2, 'food')
    setattr(category, attribute, value)
    assert getattr(category, attribute) == value


def test_budgetcategory_initialization():
    now = datetime.now()
    bcategory = BudgetCategory('food', 'expense', now, now, 105.75, 34.50, 'monthly', True, 2, 1, 1)
    assert bcategory.name == 'food'
    assert bcategory.type == 'expense'
    assert bcategory.created_at == now
    assert bcategory.updated_at == now
    assert bcategory.budget_amount == 105.75
    assert bcategory.remaining_amount == 34.50
    assert bcategory.period == 'monthly'
    assert bcategory.is_active == True
    assert bcategory.parent_id == 2
    assert bcategory.category_id == 1
    assert bcategory.id == 1

def test_budgetcategory_datetime_params_to_str():
    now = datetime.now()
    bcategory = BudgetCategory('food', 'expense', now, now)
    now_str = now.strftime(DATETIME_STR_FORMAT)
    test_created_at_str = bcategory.get_created_at_str()
    test_updated_at_str = bcategory.get_updated_at_str()

    assert now_str == test_created_at_str
    assert now_str == test_updated_at_str

@pytest.mark.parametrize(
    'attribute, value',
    [
        ('name', 'cell phone'),
        ('type', 'income'),
        ('updated_at', datetime(2025, 1, 19, 12, 30, 0)),
        ('budget_amount', 45.76),
        ('period', 'weekly'),
        ('is_active', False),
        ('parent_id', 4),
        ('id', 3),
    ]
)
def test_budgetcategory_setters_and_getters(attribute, value):
    bcategory = BudgetCategory('food', 'expense', datetime.now(), datetime.now())
    setattr(bcategory, attribute, value)
    assert getattr(bcategory, attribute) == value
