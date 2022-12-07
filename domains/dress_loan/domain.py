
from domains.dress.domain import *
from domains.user.domain import *


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
        validate('value', self.value, instance_of=bool, value=False)

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class StartDate:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^\d{4}-([012][0-9])-([012][0-9]|30|31)$'))

    def __str__(self):
        return str(self.value)

@typechecked
@dataclass(frozen=True, order=True)
class EndDate:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=pattern(r'^\d{4}-([012][0-9])-([012][0-9]|30|31)$'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class DressLoan:
    id: DressLoanID
    startDate: StartDate
    endDate: EndDate
    dress: DressID
    loaner: Username
    insertBy: Username
    terminated: Terminated

