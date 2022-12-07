
from typeguard import typechecked
from dataclasses import dataclass, InitVar, field
from valid8 import validate
from validation.dataclasses import validate_dataclass
from validation.regex import pattern
from typing import Any, List
import re

from domains.dress.domain import *
from domains.user.domain import *


@typechecked
@dataclass(frozen=True, order=True)
class Number:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=1, max_value=1000)

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: str) -> 'Number':
        return Number(int(num))

@typechecked
@dataclass(frozen=True)
class DressShop:
    __items: List[Dress] = field(default_factory=list, init=False)

    def items(self) -> int:
        return len(self.__items)

    def get_items(self) -> List[Dress]:
        return self.__items

    def item(self, index: int) -> Dress:
        validate('index', index, min_value=0)
        return self.__items[index]

    def clear(self) -> None:
        self.__items.clear()

    def add_dress(self, dress: Dress) -> None:
        validate('items', self.items())
        if self.there_are_duplicates(dress):
            raise ValueError
        self.__items.append(dress)

    def there_are_duplicates(self, item) -> bool:
        for i in self.__items:
            if item.is_equal(i):
                return True
        return False

    def remove_dress(self, index: int) -> None:
        validate('index', index, min_value=1)
        for i in range(self.items()):
            get_item = self.__items[i]
            if get_item.id.value == index:
                del self.__items[i]
                return

    def change_price(self, index: int, price: Price):
        validate('index', index, min_value=0)
        for i in range(self.items()):
            get_item = self.__items[i]
            if get_item.id.value == index:
                self.remove_dress(index)
                self.__items.insert(i,
                                    Dress(get_item.id, get_item.brand.value, price, get_item.material.value,
                                          get_item.color.value, get_item.size.value, get_item.description))

    def sort_by_price(self) -> None:
        self.__items.sort(key=lambda x: x.price)