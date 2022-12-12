import pytest
from valid8 import ValidationError


from domains.dress.domain import *
from domains.dress_loan.domain import *
from domains.dress_shop.domain import *
from domains.user.domain import *


from domains.dress_loan.domain import *


"""def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)"""


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


"""def test_price_add():
    assert Price.create(9, 99).add(Price.create(0, 1)) == Price.create(10)"""


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


"""def test_password_format():
    wrong_values = ['', '<script>alert()</script>', 'asdasd.asdadf',
                    'momohaa', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Password(value)

    correct_values = ['Momohassan17?', 'A' * 25, 'A' * 8]
    for value in correct_values:
        assert Password(value).value == value
        assert Password(value).__str__() == value"""


def test_startdate_dressloan_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            StartDate(value)

def test_startdate_dressloan_format():
    wrong_values = ['22/11/1996', '1996/22/11', '1996-022-11', '']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            StartDate(value)

    correct_values = ['1996-11-22', '2000-05-07']
    for value in correct_values:
        assert StartDate(value).value == value
        assert StartDate(value).__str__() == value

def test_enddate_dressloan_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            EndDate(value)

def test_enddate_dressloan_format():
    wrong_values = ['22/11/1996', '1996/22/11', '1996-022-11', '']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            EndDate(value)

    correct_values = ['1996-11-22', '2000-05-07']
    for value in correct_values:
        assert EndDate(value).value == value
        assert EndDate(value).__str__() == value

def test_durationdays_dressloan_type():
    wrong_values = ['string', 5.0, 1001.0, 0.0]
    for value in wrong_values:
        with pytest.raises(TypeError):
            DurationDays(value)

def test_durationdays_dressloan_format():
    wrong_values = [-5, -1001, 1001, 0]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            DurationDays(value)

    correct_values = [1, 10, 100, 1000]
    for value in correct_values:
        assert DurationDays(value).value == value
        assert DurationDays(value).__str__() == value


def test_terminated_dressloan_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, "string"]
    for value in wrong_values:
        with pytest.raises(TypeError):
            Terminated(value)

def test_terminated_dressloan_format():
    correct_values = [True, False]
    for value in correct_values:
        assert Terminated(value).value == value, "Wrong value saved in Terminated class"
        assert Terminated(value).__str__() == str(value), "Wrong value on Terminated str() method"

def test_dressloanID_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            DressLoanID(value)
def test_dressloanID_format():
    """
     ba524880-b416-4997-a604-cdd37c159ee: missing last char
     33cba6b6-c36b-49/8-bed4-309249cf9bf9: use unpermitted char
     eef3d853-e2d2-4891-b036-f92cdcbcaf24o: too many values
    """
    wrong_values = ['ba524880-b416-4997-a604-cdd37c159ee','33cba6b6-c36b-49/8-bed4-309249cf9bf9', 'eef3d853-e2d2-4891-b036-f92cdcbcaf24o']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            DressLoanID(str(value))

    correct_values = ['ba524880-b416-4997-a604-cdd37c159ee1', '33cba6b6-c36b-49a8-bed4-309249cf9bf9', 'eef3d853-e2d2-4891-b036-f92cdcbcaf24']
    for value in correct_values:
        assert DressLoanID(value).value == value
        assert DressLoanID(value).__str__() == value


def test_dressID_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            DressID(value)

def test_dressID_format():
    """
     ba524880-b416-4997-a604-cdd37c159ee: missing last char
     33cba6b6-c36b-49/8-bed4-309249cf9bf9: use unpermitted char
     eef3d853-e2d2-4891-b036-f92cdcbcaf24o: too many values
    """
    wrong_values = ['ba524880-b416-4997-a604-cdd37c159ee','33cba6b6-c36b-49/8-bed4-309249cf9bf9', 'eef3d853-e2d2-4891-b036-f92cdcbcaf24o']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            DressID(str(value))

    correct_values = ['ba524880-b416-4997-a604-cdd37c159ee1', '33cba6b6-c36b-49a8-bed4-309249cf9bf9', 'eef3d853-e2d2-4891-b036-f92cdcbcaf24']
    for value in correct_values:
        assert DressID(value).value == value
        assert DressID(value).__str__() == value


def test_brand_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            Brand(value)

def test_brand_format():
    wrong_values = ['', 'ZARA', 'VERSACE']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Brand(value)

    correct_values = ['GUCCI', 'VALENTINO', 'ARMANI']
    for value in correct_values:
        assert Brand(value).value == value
        assert Brand(value).__str__() == value


def test_material_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            Material(value)
def test_material_format():
    wrong_values = ['', 'Polyester', 'Quaisasicosa']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Material(value)

    correct_values = ['WOOL', 'SILK', 'COTTON']
    for value in correct_values:
        assert Material(value).value == value
        assert Material(value).__str__() == value

def test_color_type():
    wrong_values = [-1, 0, 1, -1.0, 0.0, 1, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            Color(value)

def test_color_format():
    wrong_values = ['', 'ORANGE', 'Quaisasicosa']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Color(value)

    correct_values = ['BLACK', 'BLUE', 'GRAY']
    for value in correct_values:
        assert Color(value).value == value
        assert Color(value).__str__() == value


def test_size_type():
    wrong_values = ["string", -1.0, 0.0, 1.0, True, False]
    for value in wrong_values:
        with pytest.raises(TypeError):
            Size.create(value)

def test_size_format():
    wrong_values = [37, 61]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Size.create(value)

    correct_values = [38, 50, 60]
    for value in correct_values:
        assert Size(value).value == value
        assert Size(value).__int__() == value