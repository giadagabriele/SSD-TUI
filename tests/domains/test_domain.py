import pytest
from valid8 import ValidationError


from domains.dress.domain import *
from domains.dress_loan.domain import *
from domains.dress_shop.domain import *
from domains.user.domain import *
from domains.dress_loan.domain import *


LIST_OF_TYPEERROR_FOR_INT = ["string", -1.0, 0.0, 1.0, True, False]
LIST_OF_TYPEERROR_FOR_BOOL = ["string", -1.0, 0.0, 1.0, -1, 0, 1]
LIST_OF_TYPEERROR_FOR_STR = [-1.0, 0.0, 1.0, -1, 0, 1, True, False]
LIST_OF_TYPEERROR_FOR_LIST = ["string", -1.0, 0.0, 1.0, -1, 0, 1, True, False]




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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_INT
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
    wrong_values = LIST_OF_TYPEERROR_FOR_BOOL
    for value in wrong_values:
        with pytest.raises(TypeError):
            Terminated(value)

def test_terminated_dressloan_format():
    correct_values = [True, False]
    for value in correct_values:
        assert Terminated(value).value == value, "Wrong value saved in Terminated class"
        assert Terminated(value).__str__() == str(value), "Wrong value on Terminated str() method"

def test_dressloanID_type():
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
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
    wrong_values = LIST_OF_TYPEERROR_FOR_INT
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

def test_description_type():
    wrong_values = LIST_OF_TYPEERROR_FOR_STR
    for value in wrong_values:
        with pytest.raises(TypeError):
            Description(value)

def test_description_format():
    wrong_values = ["&", "?", "!", "~", "'", "|", "a"*101]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Description(value)

    correct_values = ["Correct description example..."]
    for value in correct_values:
        assert Description(value).value == value
        assert Description(value).__str__() == value

def test_deleted_type():
    wrong_values = LIST_OF_TYPEERROR_FOR_BOOL
    for value in wrong_values:
        with pytest.raises(TypeError):
            Deleted(value)

def test_deleted_format():
    correct_values = [True, False]
    for value in correct_values:
        assert Deleted(value).value == value
        assert Deleted(value).__str__() == str(value)

def test_price_can_not_be_negative():
    with pytest.raises(ValidationError):
        Price.create(-1)

def test_price_can_not_be_zero():
    with pytest.raises(ValidationError):
        Price.create(0)

def test_price_cents_can_not_be_negative():
    with pytest.raises(ValidationError):
        Price.create(1, -1)

def test_price_cents_can_not_be_over_99():
    with pytest.raises(ValidationError):
        Price.create(1, 100)

def test_price_with_more_then_9_cents_str():
    assert str(Price.create(15, 10)) == '15.10'

def test_price_with_less_then_10_cents_str():
    assert str(Price.create(15, 9)) == '15.9'

def test_price_without_cents_str():
    assert str(Price.create(15)) == '15.0'

def test_price_euro():
    assert Price.create(11).euro == 11
    assert Price.create(11, 0).euro == 11
    assert Price.create(11, 22).euro == 11

def test_price_cents():
    assert Price.create(11).cents == 0
    assert Price.create(11, 0).cents == 0
    assert Price.create(11, 22).cents == 22

def test_price_parse():
    assert Price.parse('9.60') == Price.create(9, 60)


def test_dress_is_equal_method_with_an_equal_dress():
    uuid = DressID("ba524880-b416-4997-a604-cdd37c159eb1")
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=uuid, brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dress2 = Dress(id=uuid, brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    assert dress1.is_equal(dress2)

def test_number_type():
    wrong_values = LIST_OF_TYPEERROR_FOR_INT
    for value in wrong_values:
        with pytest.raises(TypeError):
            DressLoanList(value)

def test_number_format():
    wrong_values = [-1, 0, 1001]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Number(value)

    correct_values = [1, 10, 100, 1000]
    for value in correct_values:
        assert Number(value).value == value
        assert Number(value).__int__() == value

def test_dressloan_list_add_and_length_methods():
    dressloan1 = DressLoan(
        uuid= DressLoanID("ba524880-b416-4997-a604-cdd37c159eb1"),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(45),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    assert dressLoanList.length() == 1

def test_dressloan_list_item_method():
    dressLoanID = "ba524880-b416-4997-a604-cdd37c159eb1"
    dressloan1 = DressLoan(
        uuid= DressLoanID(dressLoanID),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(45),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    item = dressLoanList.item(0)
    assert item.uuid.value == dressLoanID

def test_dressloan_list_items_method():
    dressLoanID = "ba524880-b416-4997-a604-cdd37c159eb1"
    dressloan1 = DressLoan(
        uuid= DressLoanID(dressLoanID),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(45),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressLoanID2 = "ba524880-b416-4997-a604-cdd37c159eb2"
    dressloan2 = DressLoan(
        uuid=DressLoanID(dressLoanID2),
        startDate=StartDate('1996-11-22'),
        endDate=EndDate('1996-11-22'),
        dressID=DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner=UserID(1),
        totalPrice=Price(45),
        loanDurationDays=DurationDays(5),
        insertBy=UserID(2),
        terminated=Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    dressLoanList.add(dressloan2)
    items = dressLoanList.items()
    assert items[0].uuid.value == dressLoanID and items[1].uuid.value == dressLoanID2

def test_dressloan_list_clear_method():
    dressLoanID = "ba524880-b416-4997-a604-cdd37c159eb1"
    dressloan1 = DressLoan(
        uuid= DressLoanID(dressLoanID),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(45),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    dressLoanList.clear()
    assert dressLoanList.length() == 0

def test_dressloan_list_there_are_duplicates_method():
    dressLoanID = "ba524880-b416-4997-a604-cdd37c159eb1"
    dressloan1 = DressLoan(
        uuid= DressLoanID(dressLoanID),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(45),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressloan2 = DressLoan(
        uuid=DressLoanID(dressLoanID),
        startDate=StartDate('1996-11-22'),
        endDate=EndDate('1996-11-22'),
        dressID=DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner=UserID(1),
        totalPrice=Price(45),
        loanDurationDays=DurationDays(5),
        insertBy=UserID(2),
        terminated=Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    assert dressLoanList.there_are_duplicates(dressloan2)

def test_dressloan_list_there_are_duplicates_method():
    dressLoanID = "ba524880-b416-4997-a604-cdd37c159eb1"
    dressloan1 = DressLoan(
        uuid= DressLoanID(dressLoanID),
        startDate= StartDate('1996-11-22'),
        endDate= EndDate('1996-11-22'),
        dressID= DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner= UserID(1),
        totalPrice= Price(2),
        loanDurationDays= DurationDays(5),
        insertBy= UserID(2),
        terminated= Terminated(False))
    dressLoanID2 = "ba524880-b416-4997-a604-cdd37c159eb2"
    dressloan2 = DressLoan(
        uuid=DressLoanID(dressLoanID2),
        startDate=StartDate('1996-11-22'),
        endDate=EndDate('1996-11-22'),
        dressID=DressID("ba524880-b416-4997-a604-cdd37c159eb1"),
        loaner=UserID(1),
        totalPrice=Price(1),
        loanDurationDays=DurationDays(5),
        insertBy=UserID(2),
        terminated=Terminated(False))
    dressLoanList = DressLoanList()
    dressLoanList.add(dressloan1)
    dressLoanList.add(dressloan2)
    assert dressLoanList.items()[0].uuid.value == dressLoanID
    dressLoanList.sort_by_total_price()
    assert dressLoanList.items()[0].uuid.value == dressLoanID2

"""     DressList     """

def test_dresslist_length_and_add_methods():
    uuid = DressID("ba524880-b416-4997-a604-cdd37c159eb1")
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=uuid, brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)
    assert dressList.length() == 1

def test_dresslist_item_method():
    uuid_for_test = "ba524880-b416-4997-a604-cdd37c159eb1"
    uuid = DressID(uuid_for_test)
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=uuid, brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)
    assert dressList.item(0).id.value == uuid_for_test

def test_dresslist_items_method():
    uuid_for_test1 = "ba524880-b416-4997-a604-cdd37c159eb1"
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=DressID(uuid_for_test1), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    uuid_for_test2 = "ba524880-b416-4997-a604-cdd37c159eb2"
    dress2 = Dress(id=DressID(uuid_for_test2), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)
    dressList.add(dress2)
    assert dressList.items()[0].id.value == uuid_for_test1 and dressList.items()[1].id.value == uuid_for_test2

def test_dresslist_clear_method():
    uuid_for_test1 = "ba524880-b416-4997-a604-cdd37c159eb1"
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=DressID(uuid_for_test1), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    uuid_for_test2 = "ba524880-b416-4997-a604-cdd37c159eb2"
    dress2 = Dress(id=DressID(uuid_for_test2), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)
    dressList.add(dress2)
    dressList.clear()
    assert dressList.length() == 0

def test_dresslist_there_are_duplicates_method():
    uuid_for_test = "ba524880-b416-4997-a604-cdd37c159eb1"
    brand = Brand("VALENTINO")
    price = Price.create(15, 5)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=DressID(uuid_for_test), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)

    dress2 = Dress(id=DressID(uuid_for_test), brand=brand, price=price, material=material, color=color, size=size,
                   description=description, deleted=deleted)

    assert dressList.there_are_duplicates(dress2)

def test_dresslist_sort_method():
    uuid_for_test1 = "ba524880-b416-4997-a604-cdd37c159eb1"
    brand = Brand("VALENTINO")
    price1 = Price.create(20)
    material = Material("COTTON")
    color = Color("BLACK")
    size = Size(40)
    description = Description("This is a description")
    deleted = Deleted(False)
    dress1 = Dress(id=DressID(uuid_for_test1), brand=brand, price=price1, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList = DressList()
    dressList.add(dress1)

    uuid_for_test2 = "ba524880-b416-4997-a604-cdd37c159eb2"
    price2 = Price.create(15)
    dress2 = Dress(id=DressID(uuid_for_test2), brand=brand, price=price2, material=material, color=color, size=size,
                   description=description, deleted=deleted)
    dressList.add(dress2)

    assert dressList.item(0).id.value == uuid_for_test1
    dressList.sort_by_price()
    assert dressList.item(0).id.value == uuid_for_test2