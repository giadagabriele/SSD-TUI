import sys
from logging import Handler
from pathlib import Path
from unittest.mock import patch, mock_open, Mock, call
import responses
import pytest

from domains.dress_shop.app import App


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


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['commesso1', '234234234'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_password(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('This user does not exist!\n')


@responses.activate
@patch('builtins.input', side_effect=['commesso1', 'Gift-Contort-Revert5'])
@patch('builtins.print')
def test_login(mocked_print, mocked_input):
    # TODO: duplicate
    responses.add(**{
        'method': responses.POST,
        'url': 'https://ssd.pingflood.tk/api/v1/auth/login/',
        'data': '{"username": "commesso1"}, {"password":Gift-Contort-Revert5}',
        'status': 200,
        'Verify': 'True',
    })
    with patch('builtins.open', mock_open()):
        App().run()
        mocked_print.assert_any_call('Login success')
        mocked_input.assert_called()
