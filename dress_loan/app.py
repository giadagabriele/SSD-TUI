from getpass import getpass
from wsgiref import headers

import csv
import sys
from pathlib import Path
from typing import Tuple, Callable, Any
import requests

from valid8 import validate, ValidationError

from domain import DressShop, Username, Password, Email, Price, Number

from menu import Menu, MenuDescription, Entry

api_server = 'https://ssd.pingflood.tk/api/v1/'


class App:
    __filename = Path(__file__).parent.parent / 'shoppingList.csv'
    __delimiter = '\t'
    __logged = False
    __key = None
    __id_dictionary = []

    def __init__(self):
        self.__first_menu = self.init_first_menu()
        self.id_user = None
        self.__commesso_menu = self.__init_commesso_menu()
        self.__client_menu = self.__init_client_menu()
        self.__dressesList = None

    def init_first_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dresses Shop '),
                            auto_select=lambda: print('Welcome please select an option!')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye Bye!'), is_exit=True)) \
            .build()

    def __init_commesso_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Welcome to our Dresses Shop App'),
                            auto_select=lambda: self.__print_items()) \
            .build()

    def __init_client_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Welcome to our Dresses Shop App'),
                            auto_select=lambda: self.__print_items()) \
            .build()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def __run(self) -> None:
        while not self.__first_menu.run() == (True, False):
            try:
                self.__fetch()
            except ValueError as e:
                print('Continuing with an empty list of fields...')
            except RuntimeError:
                print('Failed to connect to the server! Try later!')
                return
            self.__menu.run()

    def __login(self) -> bool:
        done = False
        while not done:
            username = self.__read("Username ", Username)
            if username.value == '0':
                return False

            password = self.__read("Password ", Password)
            if password.value == '0':
                return False

            res = requests.post(url=f'{api_server}auth/login/', data={'username': username, 'password': password})
            print(res.status_code)
            if res.status_code != 200:
                print('This user does not exist!')
            else:
                self.__key = res.json()['key']
                print('Login success')
                done = True
        return True

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                if prompt != 'Password':
                    line = input(f'{prompt}: ')
                else:
                    line = input(f'{prompt}: ')

                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
