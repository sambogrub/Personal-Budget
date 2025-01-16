"""This holds the base models for transactions, accounts, and budgeting categories"""

from datetime import datetime

class Transaction:
    def __init__(self, date: datetime,
                 amount: float,
                 account: int,
                 category: str=None,
                 description: str=None,
                 id: int=None,
                 type: str=None
                 ):
        self._id = id
        self._date = date
        self._type = type or self.determine_type()
        self._amount = amount
        self._account = account
        self._category = category
        self._description = description

    def determine_type(self):
        return 'income' if self.amount >= 0 else 'expense'
    
    @property
    def type(self):
        return self._type
    

class Account:
    def __init__(self,
                 name: str,
                 type: str,
                 id: int=None,
                 balance:int = 0
                 ):
        self._id = id
        self._name = name
        self._type = type
        self._balance = balance


class Category:
    def __init__(self,
                 id: int,
                 name: str,
                 parent_id: int=0
                 ):
        self._id = id
        self._name = name
        self._parent_id = parent_id


class BudgetCategory:
    def __init__(self,
                 name: str,
                 type: str,
                 parent_id: int,
                 created_at: datetime,  
                 updated_at: datetime,              
                 budget_amount: float=0,
                 remaining_amount: float=0,
                 period: str='monthly',
                 is_active: bool=True
                 ):
        self._name = name
        self._type = type
        self._parent_id = parent_id
        self._created_at = created_at
        self._updated_at = updated_at
        self._budget_amount = budget_amount
        self._remaining_amount = remaining_amount
        self._period = period
        self._is_active = is_active