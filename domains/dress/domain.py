from typeguard import typechecked
from dataclasses import dataclass
from valid8 import validate
from validation.dataclasses import *
from validation.regex import pattern
import re


REGEX_DRESS_ID = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
REGEX_BRAND = "^(GUCCI|ARMANI|VALENTINO)$"
REGEX_MATERIAL = "^(WOOL|SILK|COTTON)$"
REGEX_COLOR = "^(BLACK|BLUE|WHITE|RED|PINK|GRAY)$"
REGEX_DATE = "^\d{4}-([012][0-9])-([012][0-9]|30|31)$"
REGEX_DESCRIPTION = "^[A-Za-z0-9\s.,_-]*$"
REGEX_PRICE = "(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?"
MIN_SIZE = 38
MAX_SIZE = 60
MAX_VALUE_PRICE = 1000000
MAX_VALUE_PRICE_CENT = 99
MIN_VALUE_PRICE_CENT = 0
MIN_VALUE_PRICE = 1

@typechecked
@dataclass(frozen=True, order=True)
class DressID:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_DRESS_ID))

    def __str__(self):
        return self.value

    @staticmethod
    def create(uuid: str) -> 'DressID':
        return DressID(int(uuid))


@typechecked
@dataclass(frozen=True, order=True)
class Brand:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_BRAND))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Material:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_MATERIAL))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Color:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_COLOR))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class Size:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate_size_step(self.value)
        validate('value', self.value, min_value=MIN_SIZE, max_value=MAX_SIZE)

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: int) -> 'Size':
        return Size(num)


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100,
                 custom=pattern(REGEX_DESCRIPTION))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class Deleted:
    value: bool

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, instance_of=bool)

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int

    __min_value = MIN_VALUE_PRICE
    __min_cent_value = MIN_VALUE_PRICE_CENT
    __max_value = MAX_VALUE_PRICE
    __max_cent_value = MAX_VALUE_PRICE_CENT
    __parse_pattern = re.compile(REGEX_PRICE)

    def __post_init__(self):
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=self.__min_value, max_value=self.__max_value)

    def __str__(self):
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100}'

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=Price.__min_value, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=Price.__min_cent_value, max_value=Price.__max_cent_value)
        return Price(euro * 100 + cents)

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

    """def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)"""


@typechecked
@dataclass(order=True)
class Dress:
    id: DressID
    brand: Brand
    price: Price
    material: Material
    color: Color
    size: Size
    description: Description
    deleted: Deleted

   
    def is_equal(self, other):
        return isinstance(other,
                          Dress) and self.id.value == other.id.value 


