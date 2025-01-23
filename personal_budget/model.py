"""This holds the base models for transactions, accounts, and budgeting categories"""

from datetime import datetime

from personal_budget.config import DATETIME_STR_FORMAT

class Transaction:
    def __init__(self, 
                 date: datetime,
                 amount: float,
                 account: int=None, #account id number matching database account number
                 category: int=None, #category id number matcing database category number
                 description: str=None,
                 id: int=None, #id number matching database id number
                 type: str=None #income or expense
                 ):
        self._id = id
        self._date = date
        self._amount = amount
        self._type = type or self.determine_type()
    
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
        return 'income' if self._amount >= 0 else 'expense'
    
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
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_):
        if self._id == None:
            self._id = id_

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
                 type: str, #checking, savings, credit
                 id: int=None,
                 balance: float=0.0
                 ):
        self._id = id
        self._name = name
        self._type = type
        self._balance = balance

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name_: str):
        self._name = name_

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type_: str):
        self._type = type_

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_: int):
        if self._id == None:
            self._id = id_

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, balance_: float):
        self._balance = balance_


class Category:
    def __init__(self,
                name: str,
                parent_id: int=None,
                id: int=None
                ):
        self._id = id
        self._name = name
        self._parent_id = parent_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_: str):
        self._name = name_

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_: int):
        if self._id == None:
            self._id = id_

    @property
    def parent_id(self):
        return self._parent_id
    
    @parent_id.setter
    def parent_id(self, id_):
        self._parent_id = id_

class BudgetCategory:
    def __init__(self,
                 name: str,
                 type: str, # income or expense
                 created_at: datetime,  
                 updated_at: datetime,              
                 budget_amount: float=0,
                 remaining_amount: float=0,
                 period: str='monthly',
                 is_active: bool=True,
                 parent_id: int=None, #id that references a parent category
                 category_id: int=None,
                 id: int=None
                 ):
        self._name = name
        self._type = type
        self._parent_id = parent_id
        self._category_id = category_id
        self._id = id
        self._created_at = created_at
        self._updated_at = updated_at
        self._budget_amount = budget_amount
        self._remaining_amount = remaining_amount
        self._period = period
        self._is_active = is_active

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name_: str):
        self._name = name_

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type_: str):
        self._type = type_

    @property
    def created_at(self):
        return self._created_at
    
    def get_created_at_str(self) -> str:
        created_at_str = self._created_at.strftime(DATETIME_STR_FORMAT)
        return created_at_str
    
    @property
    def updated_at(self):
        return self._updated_at
    
    @updated_at.setter
    def updated_at(self, timestamp: datetime):
        self._updated_at = timestamp

    def get_updated_at_str(self) -> str:
        updated_at_str = self._updated_at.strftime(DATETIME_STR_FORMAT)
        return updated_at_str

    @property
    def budget_amount(self):
        return self._budget_amount
    
    @budget_amount.setter
    def budget_amount(self, amount: float):
        self._budget_amount = amount

    @property
    def remaining_amount(self):
        return self._remaining_amount
    
    @property
    def period(self):
        return self._period
    
    @period.setter
    def period(self, period_: str):
        self._period = period_

    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, state: bool):
        self._is_active = state

    @property
    def parent_id(self):
        return self._parent_id
    
    @parent_id.setter
    def parent_id(self, id_: int):
        self._parent_id = id_

    @property
    def category_id(self):
        return self._category_id
    
    @category_id.setter
    def category_id(self, id_: int):
        self._category_id = id_

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_: int):
        if self._id == None:
            self._id = id_

