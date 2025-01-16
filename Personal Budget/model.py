"""This holds the base models for transactions, accounts, and budgeting categories"""

from datetime import datetime

class Transaction:
    def __init__(self, date: datetime,
                 amount: float,
                 account: int=None, #account id number matching database account number
                 category: int=None, #category id number matcing database category number
                 description: str=None,
                 id: int=None, #id number matching database id number
                 type: str=None
                 ):
        self._id = id
        self._date = date
        self._type = type or self.determine_type()
        self._amount = amount
        self._account = account
        self._category = category
        self._description = description

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date_: datetime):
        self._date = date_

    def determine_type(self):
        return 'income' if self.amount >= 0 else 'expense'
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, label: str):
        self._type = label

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount_: float):
        self._amount = amount_

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category_: int):
        self._category = category_

    @property
    def account(self):
        return self._account
    
    @account.setter
    def account(self, account_: int):
        self._account = account_

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description_: str):
        self._description = description_

    @description.deleter
    def description(self):
        self.description = None    
    

class Account:
    def __init__(self,
                 name: str,
                 type: str,
                 id: int=None,
                 balance: int=0
                 ):
        self._id = id
        self._name = name
        self._type = type
        self._balance = balance

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name_):
        self._name = name_

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type_):
        self._type = type_

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, balance_):
        self.balance = balance_


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