import pytest
from valid8 import ValidationError


from domains.dress.domain import *
from domains.user.domain import *

from domains.dress_loan.domain import *


def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_can_not_be_negative():
    with pytest.raises(ValidationError):
        Price.create(-1, 0)


def test_price_0_cents():
    assert Price.create(1, 0) == Price.create(1)


def test_price_str():
    assert str(Price.create(15, 99)) == '15.99'


def test_price_euro():
    assert Price.create(11, 22).euro == 11


def test_price_parse():
    assert Price.parse('9.60') == Price.create(9, 60)


def test_price_cents():
    assert Price.create(11, 22).cents == 22


def test_price_add():
    assert Price.create(9, 99).add(Price.create(0, 1)) == Price.create(10)


def test_username_format():
    wrong_values = ['', '_ciao_', '<script>alert()</script>', 'uno spazio', 'è nonvabene', '%', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Username(value)

    correct_values = ['Momo1996', 'Momohassan', 'A' * 25]
    for value in correct_values:
        assert Username(value).value == value
        assert Username(value).__str__() == value


def test_email_format():
    wrong_values = ['', '_ciao@gmail.com', 'momo@libero290.com', '...@gmail.com', 'x<>@asdkjasld.89it',
                    'momo.hassan@', 'mario@gmail', 'x@gmx.', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Email(value)

    correct_values = ['momohassan96@gmail.com', 'momohassan@libero.it', 'momo.hassan@gmail.com',
                      'A' * 20 + '@' + 'a.it']
    for value in correct_values:
        assert Email(value).value == value
        assert Email(value).__str__() == value


def test_password_format():
    wrong_values = ['', '<script>alert()</script>', 'asdasd.asdadf',
                    'momohaa', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Password(value)

    correct_values = ['Momohassan17?', 'A' * 25, 'A' * 8]
    for value in correct_values:
        assert Password(value).value == value
        assert Password(value).__str__() == value


def test_brand_format():
    wrong_values = ['', 'ZARA', 'VERSACE']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Brand(value)

    correct_values = ['GUCCI', 'VALENTINO', 'ARMANI']
    for value in correct_values:
        assert Brand(value).value == value
        assert Brand(value).__str__() == value


def test_material_format():
    wrong_values = ['', 'Polyester', 'Quaisasicosa']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Material(value)

    correct_values = ['WOOL', 'SILK', 'COTTON']
    for value in correct_values:
        assert Material(value).value == value
        assert Material(value).__str__() == value


def test_color_format():
    wrong_values = ['', 'ORANGE', 'Quaisasicosa']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Color(value)

    correct_values = ['BLACK', 'BLUE', 'GRAY']
    for value in correct_values:
        assert Color(value).value == value
        assert Color(value).__str__() == value


def test_size_format():
    wrong_values = [37, 61]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Size.create(str(value))

    correct_values = [38, 50, 60]
    for value in correct_values:
        assert Size(value).value == value
        assert Size(value).__int__() == value


def test_date_format():
    wrong_values = ['22/11/1996', '1996/22/11', '1996-022-11', '']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Date(str(value))

    correct_values = ['1996-11-22', '2000-05-07']
    for value in correct_values:
        assert Date(value).value == value
        assert Date(value).__str__() == value


"""def test_num_cannot_be_negative_or_zero():
    wrong_values = [-2, 0]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Number.create(str(value))
    correct_values = [1, 150]
    for value in correct_values:
        assert Number(value).__int__() == value"""
