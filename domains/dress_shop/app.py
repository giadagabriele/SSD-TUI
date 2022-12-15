import csv
import getpass
import json
import os
import re
import sys
import uuid
from getpass import getpass
from pathlib import Path
from typing import Any, Callable, Tuple
from wsgiref import headers

import jwt
import requests
from jwt.algorithms import get_default_algorithms
from rich.console import Console
from rich.status import Status
from rich import inspect
from valid8 import ValidationError, validate

from domains.dress.domain import *
from domains.dress_loan.menu import Entry, Menu, MenuDescription
from domains.dress_shop.domain import *
from domains.user.domain import *
from settings import *

api_server = settings['BASE_URL']


class App:
    __key = None
    __refreshKey = None
    __userID = None
    __role = None
    __username = None
    __console = None

    def __init__(self):
        self.__console = Console()
        self.__first_menu = self.init_first_menu()
        self.id_user = None
        self.__choice_menu = self.init_choice_menu()
        self.__dressloan_menu_commessi = self.init_dressloan_menu_commessi()
        self.__dressloan_menu_user = self.init_dressloan_menu_user()
        self.__dress_menu_commessi = self.init_dress_menu_commessi()
        self.__dress_menu_user = self.init_dress_menu_user()
        self.__dressList = DressList()
        self.__dressloanList = DressLoanList()
        get_default_algorithms()

    def exit_function(self):
        print('Bye Bye!\n')
        self.exit_from_app()

    def exit_from_app(self):
        exit()

    def init_first_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy'),
                            auto_select=lambda: print('\nWelcome! Please select an option\n')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.login())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.exit_function())) \
            .build()

    def init_choice_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Choice Menu'),
                            auto_select=lambda: print('\nSelect the menu to display\n')) \
            .with_entry(Entry.create('1', 'Dress Loan', on_selected=lambda: self.run_dressloan_menu())) \
            .with_entry(Entry.create('2', 'Dress', on_selected=lambda: self.run_dress_menu())) \
            .with_entry(Entry.create('3', 'Logout', on_selected=lambda: self.logout())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.exit_function())) \
            .build()

    def init_dressloan_menu_commessi(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Dress Loan Menu'),
                            auto_select=lambda: self.print_dressloans()) \
            .with_entry(
            Entry.create('1', 'Sort by total price', on_selected=lambda: self.__dressloanList.sort_by_total_price())) \
            .with_entry(Entry.create('2', 'Extend loan', on_selected=lambda: self.edit_dressloan_end_date())) \
            .with_entry(Entry.create('3', 'Close loan', on_selected=lambda: self.remove_dressloan())) \
            .with_entry(Entry.create('0', 'Back', is_exit=True)) \
            .build()

    def init_dressloan_menu_user(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Dress Loan Menu'),
                            auto_select=lambda: self.print_dressloans()) \
            .with_entry(
            Entry.create('1', 'Sort by total price', on_selected=lambda: self.__dressloanList.sort_by_total_price())) \
            .with_entry(Entry.create('0', 'Back', is_exit=True)) \
            .build()

    def init_dress_menu_commessi(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Dress Menu'),
                            auto_select=lambda: self.print_dresses()) \
            .with_entry(Entry.create('1', 'Sort by price', on_selected=lambda: self.__dressList.sort_by_price())) \
            .with_entry(Entry.create('2', 'Add dress', on_selected=lambda: self.add_dress())) \
            .with_entry(Entry.create('3', 'Edit dress price', on_selected=lambda: self.edit_dress_price())) \
            .with_entry(Entry.create('4', 'Make dress unavailable', on_selected=lambda: self.remove_dress())) \
            .with_entry(Entry.create('5', 'Reserve', on_selected=lambda: self.add_dressloan())) \
            .with_entry(Entry.create('0', 'Back', is_exit=True)) \
            .build()

    def init_dress_menu_user(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Dress Menu'),
                            auto_select=lambda: self.print_dresses()) \
            .with_entry(Entry.create('1', 'Sort by price', on_selected=lambda: self.__dressList.sort_by_price())) \
            .with_entry(Entry.create('2', 'Reserve', on_selected=lambda: self.add_dressloan())) \
            .with_entry(Entry.create('0', 'Back', is_exit=True)) \
            .build()

    def run(self) -> None:
        try:
            self.__run()
        except KeyboardInterrupt:
            self.__console.print("\nBye!")
            sys.exit()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def fetch_methods(self) -> None:
        try:
            self.fetch_dress()
            self.fetch_dressloan()
        except ValueError as e:
            print(e)
        except RuntimeError:
            print('Failed to connect to the server! Try later!')
            return

    def __run(self) -> None:
        if not self.login():
            while not self.__first_menu.run() == (True, False):
                pass
        self.fetch_methods()
        self.__choice_menu.run()

    def run_dressloan_menu(self) -> None:
        if self.__role == 'commessi':
            self.__dressloan_menu_commessi.run()
        elif self.__role == 'user':
            self.__dressloan_menu_user.run()

    def run_dress_menu(self) -> None:
        if self.__role == 'commessi':
            self.__dress_menu_commessi.run()
        elif self.__role == 'user':
            self.__dress_menu_user.run()

    def login(self) -> bool:
        done = False
        while not done:
            username = self.read("Username ", Username)
            if username.value == '0':
                return False
            password = self.read("Password ", Password)
            if password.value == '0':
                return False

            res = requests.post(url=f'{api_server}/login/', data={'username': username, 'password': password},
                                verify=True)

            if res.status_code != 200:
                print('This user does not exist!\n')
            else:
                self.__key = res.json()['access']
                print('Login succeed\n')
                self.decode_token_role(self.__key)
                done = True
        return True

    def logout(self) -> bool:
        print("Logout!")
        self.init_first_menu().run()
        return True

    def decode_token_role(self, key):
        secret = settings['SECRET_KEY']
        decoded = jwt.decode(key, secret, algorithms=['HS512'])
        self.__userID = decoded['user_id']
        self.__role = decoded['groups'][0]
        self.__username = decoded['username']

    @staticmethod
    def read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print('Format not satisfied\n')

    def fetch_dress(self) -> None:
        self.__dressList.clear()
        res = requests.get(url=f'{api_server}/dress/', verify=True, headers={'Authorization': f'Bearer {self.__key}'})
        if res.status_code != 200:
            raise RuntimeError()

        json = res.json()

        if json is None:
            return
        for item in json:
            uuid = DressID(str(item['id']))
            brand = Brand(str(item['brandType']))
            price = Price.create(int(int(item['priceInCents']) / 100), int(item['priceInCents']) % 100)
            material = Material(str(item['materialType']))
            color = Color(str(item['colorType']))
            size = Size(int(item['size']))
            description = Description(str(item['description']))
            deleted = Deleted(bool(item['deleted']))
            dress = Dress(uuid, brand, price, material, color, size, description, deleted)
            self.__dressList.add(dress)

    def fetch_dressloan(self) -> None:
        self.__dressloanList.clear()
        res = requests.get(url=f'{api_server}/loan/',
                           headers={'Authorization': f'Bearer {self.__key}'}, verify=True)
        if res.status_code != 200:
            raise RuntimeError()

        json = res.json()
        if json is None:
            return

        for item in json:
            uuidDressLoan = DressLoanID(str(item['id']))
            startDate = StartDate(str(item['startDate']))
            endDate = EndDate(str(item['endDate']))
            dressID = DressID(str(item['dress']))
            loaner = UserID(int(item['loaner']))
            totalPrice = Price(int(item['totalPrice']))
            loanDurationDays = DurationDays(int(item['loanDurationDays']))
            insertBy = UserID(int(item['insertBy']))
            terminated = Terminated(bool(item['terminated']))
            dressloan = DressLoan(uuidDressLoan, startDate, endDate, dressID, loaner, totalPrice, loanDurationDays,
                                  insertBy, terminated)
            self.__dressloanList.add(dressloan)

    def print_dressloans(self) -> None:
        if self.__dressloanList.length() == 0:
            return
        print_sep = lambda: print('-' * 180)
        print_sep()
        fmt = '%-10s %-30s  %-20s  %-20s %-30s %-20s %-10s'
        print(fmt % (
        'Number', 'Start-Date', 'End-Date', 'Total Price', 'Duration Days', 'Loaner ID', 'Terminated'))  # description?
        print_sep()
        for index in range(self.__dressloanList.length()):
            item = self.__dressloanList.item(index)
            print(fmt % (index + 1, item.startDate.value, item.endDate.value,
                         item.totalPrice.__str__(), item.loanDurationDays.value, item.loaner.value,
                         item.terminated.value))
        print_sep()

    def print_dresses(self) -> None:
        if self.__dressList.length() == 0:
            return
        print_sep = lambda: print('-' * 180)
        print_sep()
        fmt = '%-10s %-20s  %-20s  %-20s %-20s %-20s %-30s %-10s'
        print(fmt % ('Number', 'Brand', 'Price', 'Material', 'Color', 'Size', 'Description', 'Deleted'))
        print_sep()
        for index in range(self.__dressList.length()):
            item = self.__dressList.item(index)
            print(fmt % (index + 1, item.brand.value, item.price.__str__(), item.material.value,
                         item.color.value, item.size.value, item.description.value, item.deleted.value))
        print_sep()

    def read_dress(self) -> Tuple[DressID, Brand, Price, Material, Color, Size, Description, Deleted]:
        dress_uuid = uuid.uuid4()
        dress_uuidStr = str(dress_uuid)
        dress_id = DressID(dress_uuidStr)  # numero tmp verrà sovrascritto con i dati aggiornati dal backend
        brand = self.read('Brand (GUCCI or ARMANI or VALENTINO)', Brand)
        correctPrice = False
        while correctPrice == False:
            try:
                eur = self.read('Eur: ', int)
                cents = self.read('Cents: ', int)
                price = Price.create(eur, cents)
                correctPrice = True
            except ValidationError:
                print("Format not satisfied\n")
                correctPrice = False
        material = self.read('Material (WOOL or SILK or COTTON)', Material)
        color = self.read('Color (BLACK or BLUE or WHITE or RED or PINK or GRAY)', Color)
        correctSize = False
        while correctSize == False:
            try:
                size = self.read('Size (from 38 to 60)', int)
                real_size = Size(size)
                correctSize = True
            except ValidationError:
                print("Format not satisfied\n")
                correctSize = False
        description = self.read('Description', Description)
        deleted = Deleted(False)
        return dress_id, brand, price, material, color, real_size, description, deleted


    def read_dressloan(self) -> Tuple[
        DressLoanID, StartDate, EndDate, DressID, UserID, Price, DurationDays, UserID, Terminated]:
        loan_uuid = uuid.uuid4()
        loan_uuidStr = str(loan_uuid)
        loan_id = DressLoanID(loan_uuidStr)  # numero tmp verrà sovrascritto con i dati aggiornati dal backend
        start_date = self.read('Start Date (format yyyy-mm-dd)', StartDate)
        end_date = self.read('End Date (format yyyy-mm-dd)', EndDate)
        dress_uuid = uuid.uuid4()
        dress_uuidStr = str(dress_uuid)
        dress_id = DressID(dress_uuidStr)  # numero tmp verrà sovrascritto tramite indice di dress
        correctLoaner = False
        while correctLoaner == False:
            try:
                loaner_id = self.read('Loaner (if you are a user PRESS ENTER)', str)
                if loaner_id == "":
                    loaner_id = self.__userID
                if int(loaner_id) < 1 :
                    raise ValidationError(
                        ("Format not satisfied\n"),
                        var_value=loaner_id,
                        var_name="loaner_id",
                        failure=ValidationFailure(loaner_id)
                    )
                correctLoaner = True
            except ValidationError:
                print("Format not satisfied\n")
                correctLoaner = False
        real_loaner_id = UserID(int(loaner_id))
        total_price = Price(125)  # numero tmp verrà sovrascritto con i dati aggiornati dal backend
        duration_days = DurationDays(2)  # numero tmp verrà sovrascritto con i dati aggiornati dal backend
        insertby_id = UserID(3)  # numero tmp verrà sovrascritto tramite login
        terminated = Terminated(False)
        return loan_id, start_date, end_date, dress_id, real_loaner_id, total_price, duration_days, insertby_id, terminated

    def add_dress(self) -> None:
        newDress = Dress(*self.read_dress())

        newDressJSON = {
            "brandType": newDress.brand.value,
            "priceInCents": newDress.price.value_in_cents,
            "materialType": newDress.material.value,
            "colorType": newDress.color.value,
            "size": newDress.size.value,
            "description": newDress.description.value,
            "deleted": newDress.deleted.value,
        }

        res = requests.post(url=f'{api_server}/dress/', json=newDressJSON, verify=True,
                            headers={'Authorization': f'Bearer {self.__key}'})

        if res.status_code == 201:
            self.fetch_dress()
            print('Dress added!')
            input("PRESS ENTER TO CONTINUE")

        else:
            print(res.json()[list(res.json().keys())[0]])
            input("PRESS ENTER TO CONTINUE")

    def remove_dress(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)

        index = self.read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        oldDress = self.__dressList.item(index - 1)

        res = requests.delete(url=f'{api_server}/dress/{oldDress.id.value}', verify=True,
                              headers={'Authorization': f'Bearer {self.__key}'})

        if res.status_code == 204:
            self.fetch_dress()
            print('Dress marked as unavailable!\n')
            input("PRESS ENTER TO CONTINUE")
        else:
            print(res.json()[list(res.json().keys())[0]])
            input("PRESS ENTER TO CONTINUE")

    def edit_dress_price(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)

        index = self.read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        edited_dress = self.__dressList.item(index - 1)
        correctPrice = False
        edited_price = None
        while correctPrice == False:
            try:
                eur = self.read('Eur: ', int)
                cents = self.read('Cents: ', int)
                edited_price = Price.create(eur, cents)
                correctPrice = True
            except ValidationError:
                print("Format not satisfied\n")
                correctPrice = False

        newEditedDressJSON = {
            "brandType": edited_dress.brand.value,
            "priceInCents": int(edited_price),
            "materialType": edited_dress.material.value,
            "colorType": edited_dress.color.value,
            "size": edited_dress.size.value,
            "description": edited_dress.description.value,
            "deleted": edited_dress.deleted.value,
        }

        res = requests.put(url=f'{api_server}/dress/{edited_dress.id.value}', json=newEditedDressJSON, verify=True,
                           headers={'Authorization': f'Bearer {self.__key}'})

        self.fetch_dress()
        if res.status_code == 200:
            print('Dress price edited!\n')
            input("PRESS ENTER TO CONTINUE")
        else:
            print(res.json()[list(res.json().keys())[0]])
            input("PRESS ENTER TO CONTINUE")


    def add_dressloan(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)

        index = self.read('Index (0 to cancel)', builder)
        if index == 0:
            print('Selected!\n')
            return
        dress_selected = self.__dressList.item(index - 1)
        newDressLoan = DressLoan(*self.read_dressloan())
        newDressLoan.dressID = DressID(dress_selected.id.value)
        newDressLoan.insertBy = UserID(self.__userID)
        newDressLoanJSON = {
            "startDate": newDressLoan.startDate.value,
            "endDate": newDressLoan.endDate.value,
            "dress": newDressLoan.dressID.value,
            "loaner": newDressLoan.loaner.value,
        }
        res = requests.post(url=f'{api_server}/loan/', json=newDressLoanJSON, verify=True,
                            headers={'Authorization': f'Bearer {self.__key}'})
    
        if res.status_code == 201:
            self.fetch_dressloan()
            print('Reserved!\n')
            input("PRESS ENTER")
        else:
            print(str(res.json()[list(res.json().keys())[0]]))
            input("PRESS ENTER")

    def remove_dressloan(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressloanList.length())
            return int(value)

        index = self.read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        oldDressLoan = self.__dressloanList.item(index - 1)

        res = requests.delete(url=f'{api_server}/loan/{oldDressLoan.uuid.value}', verify=True,
                              headers={'Authorization': f'Bearer {self.__key}'})

        if res.status_code == 204:
            self.fetch_dressloan()
            print('Dress loan marked as deleted!\n')
            input("PRESS ENTER TO CONTINUE")
        else:
            print(res.json()[list(res.json().keys())[0]])
            input("PRESS ENTER TO CONTINUE")

    def edit_dressloan_end_date(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressloanList.length())
            return int(value)

        index = self.read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        edited_dressloan = self.__dressloanList.item(index - 1)
        edited_end_date = self.read('End Date (format yyyy-mm-dd)', EndDate)

        newEditedDressLoanJSON = {
            "startDate": edited_dressloan.startDate.value,
            "endDate": str(edited_end_date),
            "dress": edited_dressloan.dressID.value,
            "loaner": edited_dressloan.loaner.value,
        }

        res = requests.put(url=f'{api_server}/loan/{edited_dressloan.uuid.value}', json=newEditedDressLoanJSON,
                           verify=True, headers={'Authorization': f'Bearer {self.__key}'})

        self.fetch_dressloan()
        if res.status_code == 200:
            print('Dress loan edited!\n')
            input("PRESS ENTER TO CONTINUE")
        else:
            print(res.json()[list(res.json().keys())[0]])
            input("PRESS ENTER TO CONTINUE")
