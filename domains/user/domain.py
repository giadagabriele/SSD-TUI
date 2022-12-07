
from typeguard import typechecked
from dataclasses import dataclass
from valid8 import validate
from validation.dataclasses import validate_dataclass
from validation.regex import pattern


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
