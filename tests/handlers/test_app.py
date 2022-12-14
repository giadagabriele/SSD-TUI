from unittest.mock import patch, mock_open, Mock, call
import responses
import pytest
import requests
from domains.dress_shop.app import App
from domains.dress_loan.domain import *
from main import main
from settings import *

api_server = settings['BASE_URL']


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


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2'])
@patch('builtins.print')
def test_app_dress_loan_add_dress(mocked_print, mocked_input):
    with patch.object(App, 'fetch_dress') as mocked_fetch_dress:
        mocked_fetch_dress.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_input.assert_called()
        mocked_print.assert_any_call('2:\tAdd dress')


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '4', '1'])
@patch('builtins.print')
def test_app_make_dress_unavailable_commesso(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Dress marked as unavailable!\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '5', '6', '2022-12-20', '2022-12-25', '3'])
@patch('builtins.print')
def test_app_reserve_commesso(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Reserved!\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', '250', 'WOOL', 'BLACK', '44', 'desc'])
@patch('builtins.print')
def test_app_add_dress_commesso(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Dress added!\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'BLABLA'])
@patch('builtins.print')
def test_app_add_dress_brand_format_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', ' '])
@patch('builtins.print')
def test_app_add_dress_price_format_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', '250', 'BLA'])
@patch('builtins.print')
def test_app_add_dress_price_material_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', '250', 'WOOL', 'color'])
@patch('builtins.print')
def test_app_add_dress_price_color_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', '250', 'WOOL', 'BLACK', '43'])
@patch('builtins.print')
def test_app_add_dress_size_format_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '2', '2', 'GUCCI', '250', 'WOOL', 'BLACK', '44', '!!!'])
@patch('builtins.print')
def test_app_add_dress_desc_format_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input',
       side_effect=['commesso1', 'Gift-Contort-Revert5', '1', '2', 'GUCCI', '250', 'WOOL', 'BLACK', '44', '!!!'])
@patch('builtins.print')
def test_app_add_dress_desc_format_error(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Format not satisfied\n')


@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5', '0'])
@patch('builtins.print')
def test_app_exit_commesso(mocked_print, mocked_input):
    with patch.object(App, 'exit_from_app') as mocked_exit:
        mocked_exit.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_has_calls([call('Bye Bye!\n')])
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
        mocked_input.assert_called()
        mocked_print.assert_any_call('1:\tSort by price')


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '1'])
@patch('builtins.print')
def test_app_fetch_dress_user(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('1:\tSort by total price')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '2', '0'])
@patch('builtins.print')
def test_app_go_back_dress_user(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_has_calls([call('0:\tBack'),
                                   call('>>>>>>>>>>>>**********************<<<<<<<<<<<<'),
                                   call('>>>>>>>>>>>> Dressy - Choice Menu <<<<<<<<<<<<'),
                                   call('>>>>>>>>>>>>**********************<<<<<<<<<<<<'),
                                   call('\nSelect the menu to display\n')])
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '1', '0', '0'])
@patch('builtins.print')
def test_app_go_back_dress_loan_user(mocked_print, mocked_input):
    with patch.object(App, 'exit_from_app') as mocked_exit:
        mocked_exit.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_has_calls([call('0:\tExit'),
                                       call('>>>>>>>>>>>>**************************<<<<<<<<<<<<'),
                                       call('>>>>>>>>>>>> Dressy - Dress Loan Menu <<<<<<<<<<<<'),
                                       call('>>>>>>>>>>>>**************************<<<<<<<<<<<<')])

        mocked_print.assert_has_calls([call('0:\tBack'),
                                       call('>>>>>>>>>>>>**********************<<<<<<<<<<<<'),
                                       call('>>>>>>>>>>>> Dressy - Choice Menu <<<<<<<<<<<<'),
                                       call('>>>>>>>>>>>>**********************<<<<<<<<<<<<'),
                                       call('\nSelect the menu to display\n')])
        mocked_input.assert_called()


@patch('builtins.input', side_effect=['user1', 'Gift-Contort-Revert5', '0'])
@patch('builtins.print')
def test_app_exit_user(mocked_print, mocked_input):
    with patch.object(App, 'exit_from_app') as mocked_exit:
        mocked_exit.return_value = True
        with patch('builtins.open', mock_open()):
            App().run()
        mocked_print.assert_has_calls([call('Bye Bye!\n')])
        mocked_input.assert_called()

