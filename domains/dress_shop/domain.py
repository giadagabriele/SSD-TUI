
from typeguard import typechecked
from dataclasses import dataclass, InitVar, field
from valid8 import validate
from validation.dataclasses import validate_dataclass
from validation.regex import pattern
from typing import Any, List
import re

from domains.dress.domain import *
from domains.user.domain import *
from domains.dress_loan.domain import *


MIN_NUMBER = 1
MAX_NUMBER = 1000
MAX_DRESS_LIST_LENGTH = 10000
MAX_DRESS_LIST_REAL_LENGTH = MAX_DRESS_LIST_LENGTH-1
MIN_DRESS_LIST_LENGTH = 0
MAX_DRESSLOAN_LIST_LENGTH = 100000
MAX_DRESSLOAN_LIST_REAL_LENGTH = MAX_DRESSLOAN_LIST_LENGTH-1
MIN_DRESSLOAN_LIST_LENGTH = 0


@typechecked
@dataclass(frozen=True, order=True)
class Number:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate_type(self.value, int)
        validate('value', self.value, min_value=MIN_NUMBER, max_value=MAX_NUMBER)

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: str) -> 'Number':
        return Number(int(num))


@typechecked
@dataclass(frozen=True)
class DressLoanList: 
    __items: List[DressLoan] = field(default_factory=list, init=False)

    def length(self) -> int:
        return len(self.__items)

    def item(self, index: int) -> DressLoan:
        validate('index', index, min_value=MIN_DRESSLOAN_LIST_LENGTH, max_value=MAX_DRESSLOAN_LIST_LENGTH)
        return self.__items[index]
    
    def items(self) -> List[DressLoan]:
        return self.__items

    def clear(self) -> None:
        self.__items.clear()

    def there_are_duplicates(self, newItem) -> bool:
        for item in self.__items:
            if newItem.is_equal(item):
                return True
        return False

    def add(self, dressLoan: DressLoan) -> None:
        validate('items', self.length(), max_value=MAX_DRESSLOAN_LIST_LENGTH)
        if self.there_are_duplicates(dressLoan):
            raise ValueError
        self.__items.append(dressLoan)

    """def remove_dressloan_by_index(self, index: int) -> None:
        validate('index', index, min_value=MIN_DRESSLOAN_LIST_LENGTH, max_value=self.length()-1)
        del self.__items[index]"""
    
    """def pop_dress_by_index(self, index: int) -> None:
        validate('index', index, min_value=MIN_DRESSLOAN_LIST_LENGTH, max_value=self.length()-1)
        old_dress = self.__items[index]
        del self.__items[index]
        return old_dress"""

    """Change price of dress in DressList[index]"""
    """def change_total_price_by_index(self, index: int, price: Price):
        old_item = self.pop_dress_by_index(index)
        self.__items.insert(index,
                            Dress(old_item.id, old_item.brand.value, price, old_item.material.value,
                            old_item.color.value, old_item.size.value, old_item.description))"""
    def sort_by_total_price(self) -> None:
        self.__items.sort(key=lambda x: x.totalPrice)



@typechecked
@dataclass(frozen=True)
class DressList:
    __items: List[Dress] = field(default_factory=list, init=False)

    def length(self) -> int:
        return len(self.__items)

    def item(self, index: int) -> Dress:
        validate('index', index, min_value=MIN_DRESS_LIST_LENGTH, max_value=MAX_DRESS_LIST_LENGTH)
        return self.__items[index]
    
    def items(self) -> List[Dress]:
        return self.__items

    def clear(self) -> None:
        self.__items.clear()

    def add(self, dress: Dress) -> None:
        validate('items', self.length(), max_value=MAX_DRESS_LIST_LENGTH)
        if self.there_are_duplicates(dress):
            raise ValueError
        self.__items.append(dress)

    def there_are_duplicates(self, newItem) -> bool:
        for item in self.__items:
            if newItem.is_equal(item):
                return True
        return False

    """def remove_dress_by_index(self, index: int) -> None:
        # L'index non deve essere inferiore a 0 o superiore alla lunghezza attuale
        validate('index', index, min_value=MIN_DRESS_LIST_LENGTH, max_value=self.length()-1)
        del self.__items[index]"""
    
    """def pop_dress_by_index(self, index: int) -> None:
        validate('index', index, min_value=MIN_DRESS_LIST_LENGTH, max_value=self.length()-1)
        old_dress = self.__items[index]
        del self.__items[index]
        return old_dress"""

    """Change price of dress in DressList[index]"""
    """def change_price_by_index(self, index: int, price: Price):
        # Controllo di index in remove_dress
        old_item = self.pop_dress_by_index(index)
        self.__items.insert(index,
                            Dress(old_item.id, old_item.brand.value, price, old_item.material.value,
                            old_item.color.value, old_item.size.value, old_item.description))"""

    def sort_by_price(self) -> None:
        self.__items.sort(key=lambda x: x.price)