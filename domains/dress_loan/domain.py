
from domains.dress.domain import *
from domains.user.domain import *


# REGEX_DRESSLOAN_ID = "^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"
# REGEX_DRESSLOAN_ID = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
REGEX_DRESSLOAN_ID = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
REGEX_DATE = "^\d{4}-([012][0-9])-([012][0-9]|30|31)$"
MIN_DURATION_DAYS = 1
MAX_DURATION_DAYS = 1000

@typechecked
@dataclass(frozen=True, order=True)
class DressLoanID:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 custom=pattern(r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$'))

    def __int__(self):
        return self.value

    @staticmethod
    def create(uuid: str) -> 'DressLoanID':
        return DressLoanID(int(uuid))


@typechecked
@dataclass(frozen=True, order=True)
class Terminated:
    value: bool

    def __post_init__(self):
        validate_dataclass(self)
        #validate('value', self.value, instance_of=bool, value=False)

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class StartDate:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_DATE))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class EndDate:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(REGEX_DATE))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class DurationDays:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=MIN_DURATION_DAYS, max_value=MAX_DURATION_DAYS)

    def __int__(self):
        return self.value


@typechecked
@dataclass(order=True)
class DressLoan:
    uuid: DressLoanID
    startDate: StartDate
    endDate: EndDate
    dressID: DressID
    loaner: UserID
    totalPrice: Price
    loanDurationDays: DurationDays 
    insertBy: UserID
    terminated: Terminated

   
    def is_equal(self, other):
        return isinstance(other,
                          DressLoan) and self.uuid.value == other.uuid.value 