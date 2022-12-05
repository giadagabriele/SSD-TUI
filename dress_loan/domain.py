import re
from dataclasses import dataclass, InitVar, field
from typing import Any, List

from typeguard import typechecked
from valid8 import validate
from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Number:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=1)

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: str) -> 'Number':
        return Number(int(num))


@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self):
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100:02}'

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=25, custom=pattern(r'[A-Za-z0-9]{8,25}|0'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=8, max_len=25,
                 custom=pattern(r'[A-Za-z0-9]+[\.]*[A-Za-z]*@[A-Za-z]+\.[a-z]+'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=25, custom=pattern(r'[A-Za-z0-9_@?/#&+-.]{8,25}|0'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Brand:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^(GUCCI|ARMANI|VALENTINO)$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Material:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^(WOOL|SILK|COTTON)$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Color:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^(BLACK|BLUE|WHITE|RED|PINK|GRAY)$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Size:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=38, max_value=60)

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: str) -> 'Size':
        return Size(int(num))


@typechecked
@dataclass(frozen=True, order=True)
class Date:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^\d{4}-([012][0-9])-([012][0-9]|30|31)$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100,
                 custom=pattern(r'^[A-Za-z0-9 .,_-]*$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Dress:
    id: Number
    brand: Brand
    price: Price
    material: Material
    color: Color
    size: Size
    description: Description

    def is_equal(self, other):
        return isinstance(other,
                          Dress) and self.brand.value == other.brand.value and other.price.value_in_cents == \
               self.price.value_in_cents


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
        if self.there_are_duplicates(Dress):
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
