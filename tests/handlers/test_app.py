from unittest.mock import patch, mock_open, Mock, call
import responses
import pytest

from domains.dress_shop.app import App
from domains.dress_loan.domain import *


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