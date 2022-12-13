from unittest.mock import patch, mock_open, Mock, call
import responses
import pytest

from domains.dress_shop.app import App
from domains.dress_loan.domain import *
from main import main


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data=[]):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_sign_in(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('>>>>>>>>>>>> Dressy <<<<<<<<<<<<')
    mocked_print.assert_any_call('\nWelcome! Please select an option\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['wr'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_format_username(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('Format not satisfied\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['commesso1', 'pass'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_format_password(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('Format not satisfied\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['commesso1', '234234234'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_password(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('This user does not exist!\n')


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5'])
@patch('builtins.print')
def test_app_sign_in_resists_right_password_for_commessi(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('\nHello, commesso1')


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '1'])
@patch('builtins.print')
def test_app_dress_loan(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_input.assert_called()
        mocked_print.assert_any_call('1:\tSort by total price')


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '1', '2', '6', '2023-01-11'])
@patch('builtins.print')
def test_app_extend_dress_loan_terminated_false(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_any_call('6          2022-12-30                      2023-01-11            6.84           '
                                     '      12                             2                    False     ')
        mocked_input.assert_called()


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '1', '2', '1', '2022-12-22'])
@patch('builtins.print')
def test_app_extend_dress_loan_terminated_true(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_any_call('1          2022-12-17                      2022-12-21            2.0            '
                                     '      4                              4                    True      ')
        mocked_input.assert_called()


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '1', '1'])
@patch('builtins.print')
def test_app_sort_by_total_price_dress_loan(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_any_call('1          2023-02-02                      2023-02-05            0.30           '
                                     '      3                              2                    True      ')
        mocked_print.assert_any_call('2          2022-12-03                      2022-12-04            0.50           '
                                     '      1                              3                    False     ')
        mocked_input.assert_called()


@patch('requests.get', side_effect=[mock_response(200, [{'id': '6c938757-8e23-4db6-a211-a1a7df9d4835',
                                                         'startDate': '2022-12-17', 'endDate': '2022-12-21',
                                                         'dress': '54416218-701a-4826-a0ad-9fb40348d802',
                                                         'loaner': 4, 'totalPrice': 200, 'loanDurationDays': 4,
                                                         'insertBy': 3, 'terminated': True},
                                                        {'id': '013bda71-3d8a-47d6-a4f4-b1bf66c0498b',
                                                         'startDate': '2022-12-14', 'endDate': '2022-12-18',
                                                         'dress': '1b9f4c64-c45f-48b1-962b-e5afdbe29f76',
                                                         'loaner': 2, 'totalPrice': 220, 'loanDurationDays': 4,
                                                         'insertBy': 2, 'terminated': True}])])
@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '1'])
@patch('builtins.print')
def test_app_load_list_format_ok(mocked_print, mocked_input, mocked_requests_get):
    with patch.object(App, 'fetch_dressloan') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_requests_get.assert_called()
            mocked_print.assert_any_call('>>>>>>>>>>>> Dressy - Dress Loan Menu <<<<<<<<<<<<')
            mocked_input.assert_called()


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5'])
@patch('builtins.print')
def test_app_sign_in_resists_right_password_for_user(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('\nHello, user1')


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '1'])
@patch('builtins.print')
def test_app_fetch_loan(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('\nHello, user1')
    mocked_print.assert_any_call('>>>>>>>>>>>> Dressy - Dress Loan Menu <<<<<<<<<<<<')


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '2'])
@patch('builtins.print')
def test_app_fetch_dress(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('\nHello, user1')
    mocked_print.assert_any_call('>>>>>>>>>>>> Dressy - Dress Menu <<<<<<<<<<<<')


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '2'])
@patch('builtins.print')
def test_app_fetch_dress(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('1:\tSort by price')


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '1'])
@patch('builtins.print')
def test_app_fetch_dress(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dressloan') as mocked_fetch_dressloan:
        mocked_fetch_dressloan.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('1:\tSort by total price')


'''
da errore se :
    - ci sono stampe con [bold] che fa parte di rich, va tolto console e lasciata una semplice print (se ti serve per testare esattamente quella stringa ovviamente, sennò lasciali)
    - il metodo che vuoi provare a mockare è privato/protected, infatti tipo fetch era __fetch, abbiamo dovuto rinominare come public togliendo __ e quindi lo puoi chiamare
      in patch object

quindi :
    testa tutti quelli pubblici, se non arriviamo alla percentuale qualcuno diventerà pubblico magicamente:)
'''
