from dataclass_type_validator import dataclass_type_validator, TypeValidationError
from valid8 import ValidationError, ValidationFailure


def validate_dataclass(data):
    try:
        dataclass_type_validator(data)
    except TypeValidationError as e:
        raise TypeError(e)

def validate_size_step(size):
    validate_type(size, int)
    if size % 2 != 0:
        raise ValidationError(
            ("The size can't be odd: %(size)s"),
            var_value=size,
            var_name="size",
            failure=ValidationFailure(size)
        )

def validate_type(data, type_of_data):
    if type(data) != type_of_data:
        raise TypeError("The type isn't correct!")