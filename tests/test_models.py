import pytest
from datetime import datetime

from personal_budget.model import Transaction, Account, Category, BudgetCategory

def test_transaction_initialization():
    now = datetime.now()
    transaction = Transaction(now, 32.48, 1, 3, 'van gas', 40, 'expense')
    assert transaction.date == now
    assert transaction.amount == 32.48
    assert transaction.account == 1
    assert transaction.category == 3
    assert transaction.description == 'van gas'
    assert transaction._id == 40
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
    assert account._id == 3
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