
from typeguard import typechecked
from dataclasses import dataclass
from valid8 import validate
from validation.dataclasses import validate_dataclass
from validation.regex import pattern


MIN_USER_ID_NUM = 1
MAX_USER_ID_NUM = 10000
MIN_PASSWORD_LEN = 1
MAX_PASSWORD_LEN = 25
REGEX_PASSWORD = "[A-Za-z0-9_@?/#&+-.]{8,25}|0"
MIN_EMAIL_LEN = 8
MAX_EMAIL_LEN = 25
REGEX_EMAIL = '[A-Za-z0-9]+[\.]*[A-Za-z]*@[A-Za-z]+\.[a-z]+'
MIN_USERNAME_LEN = 1
MAX_USERNAME_LEN = 25
REGEX_USERNAME = '[A-Za-z0-9]{8,25}|0'

@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=MIN_USERNAME_LEN, max_len=MAX_USERNAME_LEN, custom=pattern(REGEX_USERNAME))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=MIN_EMAIL_LEN, max_len=MAX_EMAIL_LEN,
                 custom=pattern(REGEX_EMAIL))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=MIN_PASSWORD_LEN, max_len=MAX_PASSWORD_LEN, custom=pattern(REGEX_PASSWORD))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class UserID:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=MIN_USER_ID_NUM, max_value=MAX_USER_ID_NUM)


